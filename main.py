from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Line
import numpy as np
import librosa
from chatbot_module import Chatbot

class MyApp(MDApp):
    message = StringProperty()

    def build(self):
        self.root = Builder.load_string(
            '''
ScrollView:
    BoxLayout:
        orientation: 'vertical'
        padding: '10dp'
        spacing: '10dp'

        MDTextField:
            id: text_field
            hint_text: "Enter your message"
            size_hint_y: None
            height: self.minimum_height
            adaptive_height: True
            on_text_validate: app.display_message()

        MDRaisedButton:
            text: "Enter"
            size_hint_y: None
            height: dp(48)
            on_release: app.display_message()

        MDLabel:
            id: message_label
            text: app.message
            size_hint_y: None
            height: self.texture_size[1]

        BoxLayout:
            id: waveform_layout
            size_hint_y: None
            height: dp(200)
'''
        )
        # Plot the audio waveform
        # Pass the path to your audio file here
        self.plot_waveform('output.mp3')

    def plot_waveform(self, audio_file):
        # Load the audio file
        data, sr = librosa.load(audio_file, sr=None)
        # Compute the waveform
        waveform = np.linspace(0, len(data) / sr, len(data))
        # Draw the waveform
        with self.root.ids.waveform_layout.canvas:
            Line(points=(0, 0, self.root.ids.waveform_layout.width, 0), width=2)
            for i in range(len(waveform) - 1):
                Line(points=(i, waveform[i], i + 1, waveform[i + 1]), width=1)

    def display_message(self):
        message_text = self.root.ids.text_field.text
        chatbot = Chatbot()
        response = chatbot.get_response(message_text)
        self.message = f"DukeGPT: {response}"

if __name__ == "__main__":
    MyApp().run()




