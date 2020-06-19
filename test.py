import cv2
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, StringProperty
from kivy.utils import platform


class WelcomeWindow(Screen):
    pass


class PhotoIntroWindow(Screen):
    pass


class PhotoWindow(Screen):

    class PhotoWindow(Screen):
        kernel_size = NumericProperty(None)
        activate_blur_flag = StringProperty(None)

        def slider_default_values(self):
            self.ids.PhotoWindow_save_button.text = 'save'
            self.ids.PhotoWindow_return_button.text = 'return'
            if not self.ids.camera.play:
                self.ids.camera.play = True

        def capture(self):
            if self.ids.PhotoWindow_save_button.text == 'save':
                self.ids.PhotoWindow_save_button.text = 'confirm'
                self.ids.PhotoWindow_return_button.text = 're-take'
                self.ids.camera.play = False
            elif self.ids.PhotoWindow_save_button.text == 'confirm':
                camera = self.ids.camera
                camera.export_to_png("original_image.png")
                self.manager.current = 'blurred_window'
                self.manager.ids.blurred_window.ids.original_image.source = 'original_image.png'

        class MyCamera(Camera):
            def __init__(self, **kwargs):
                self.index = -2
                super().__init__(**kwargs)

            def on_tex(self, *args):
                # if platform == 'android':
                #     self.texture = Texture.create(size=self.resolution,
                #                                   colorfmt='bgr')
                #     self.texture_size = list(self.texture.size)
                #     buffer = self._camera.grab_frame()
                #     frame = self._camera.decode_frame(buffer)
                # else:
                self.texture = self._camera.texture
                self.texture_size = list(self.texture.size)
                ret, frame = self._camera._device.read()
                if frame is None:
                    print("No")
                if self.parent.activate_blur_flag.state == 'down':
                    self.parent.activate_blur_flag.text = 'de-activate'
                    frame = self.process_frame(frame)
                else:
                    self.parent.activate_blur_flag.text = 'activate'
                self.texture.blit_buffer(frame.tostring(),
                                         colorfmt='bgr',
                                         bufferfmt='ubyte')
                super().on_tex()

            def process_frame(self, original_image):
                # Process frame with opencv
                hsv = cv2.cvtColor(original_image,
                                    cv2.COLOR_BGR2HSV)
                return hsv


class BlurredWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


main_kv = Builder.load_file("main.kv")


class TestCamera(App):
    def build(self):
        return main_kv

    def on_start(self):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE,
                                 Permission.WRITE_EXTERNAL_STORAGE,
                                 Permission.CAMERA])


if __name__ == '__main__':
    TestCamera().run()

