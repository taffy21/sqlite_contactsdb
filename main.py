from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior      # new to remember
from kivy.uix.recycleview.layout import LayoutSelectionBehavior     # new to remember
from kivy.uix.recycleboxlayout import RecycleBoxLayout              # new to remember
from kivy.uix.behaviors import FocusBehavior
from kivy.properties import ListProperty, BooleanProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
import sqlite3

from kivy.uix.textinput import TextInput


class SelectableLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    selected_name = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        """catch and handle view changes"""
        self.index = index
        return super().refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super().on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """respond to the selection of items in the view"""
        self.selected = is_selected
        if is_selected:
            my_dict = rv.data[index]
            entry = my_dict['text']
            list_entry = entry.split(',')
            name = list_entry[1].strip()
            self.selected_name = name
            App.get_running_app().root.selected_label = self.selected_name


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class ViewList(RecycleView):
    pass


class MyContactBox(BoxLayout):
    db_filename = 'contacts.db'
    data = ListProperty()
    #selected_label = StringProperty()
    #def __init__(self, **kwargs):
    #    super().__init__(**kwargs)
    #    self.view_records()

    def execute_db_query(self, query, parameters=()):
        with sqlite3.connect(self.db_filename) as conn:
            print('You have successfully connected to the Database')
            cursor = conn.cursor()
            query_result = cursor.execute(query, parameters)
            conn.commit()
        return query_result

    def on_add_contact_contact_button_clicked(self):
        self.add_new_contact()

    def add_new_contact(self):
        if self.new_contacts_validated():
            query = 'INSERT INTO contacts_list VALUES(NULL, ?, ?, ?)'
            parameters = (self.ids.name_input.text, self.ids.email_input.text, int(self.ids.number_input.text))
            self.execute_db_query(query, parameters)
            self.ids.name_input.text = ""
            self.ids.email_input.text = ""
            self.ids.number_input.text = ""
        else:
            pass
        self.view_records()


    def new_contacts_validated(self):

        return len(self.ids.name_input.text) != 0 and len(self.ids.email_input.text) != 0 and \
               len(self.ids.number_input.text) != 0

    def view_records(self):
        """ this function should allow me to view the records on the screen """
        query = 'SELECT * FROM contacts_list'
        contact_entries = self.execute_db_query(query)
        contacts = []
        for contact in contact_entries:
            contacts_dict = {'text': f'{contact}'}
            contacts.append(contacts_dict)
        self.ids.list_view.data = contacts

    def delete_contacts(self):
        name = self.selected_label
        name_modified = name.split("'")[1]
        query = 'DELETE FROM contacts_list WHERE name = ?'
        self.execute_db_query(query, (name_modified,))
        print(f'{name_modified} Deleted!!')
        self.view_records()

    def modify_window(self):
        p = MyPopup()
        p.open()

    def update_contacts(self, newphone, old_phone, name):
        query = 'UPDATE contacts_list SET number =? WHERE number =? and name =?'
        parameters = (newphone, old_phone, name)
        self.execute_db_query(query, parameters)
        # pop-up window should close


class MyPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Modify Entry"
        self.size_hint = (0.5, 0.5)
        g = GridLayout(cols=2)
        label_name = Label(text="Name")
        text_name = TextInput()
        label_oldnumber = Label(text="Old Number")
        text_email = TextInput()
        label_newnumber = Label(text="New Number")
        text_number = TextInput()
        b = Button(text="Edit")
        g.add_widget(label_name)
        g.add_widget(text_name)
        g.add_widget(label_oldnumber)
        g.add_widget(text_email)
        g.add_widget(label_newnumber)
        g.add_widget(text_number)
        g.add_widget(b)
        self.add_widget(g)



class MyContactApp(App):
    pass


if __name__ == "__main__":
    MyContactApp().run()


