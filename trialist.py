from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty, ObjectProperty


class Boxy(BoxLayout):
    data = ListProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.textin = TextInput(multiline=False, size_hint_y=0.2)
        self.btn = Button(text='Press Me', on_press=self.callback, size_hint_y=0.1)
        self.my_rv = RecycleView(viewclass='Label', data=[{'text': "My's One"}])
        self.rblayout = BoxLayout(orientation='vertical')
        self.my_rv.add_widget(self.rblayout)
        self.add_widget(self.textin)
        self.add_widget(self.my_rv)
        self.add_widget(self.btn)

    def callback(self, instance):
        self.data.append({"text": self.textin.text})
        self.my_rv.data = self.data
        print(self.my_rv.data)



class MyApp(App):
    def build(self):
        r = Boxy()
        return r


if __name__ == "__main__":
    MyApp().run()



