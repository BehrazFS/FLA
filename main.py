from queue import Queue
from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ListProperty, ObjectProperty, NumericProperty, ReferenceListProperty, StringProperty
from kivy.utils import rgba
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ListProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.base import ExceptionHandler, ExceptionManager

Builder.load_file('front.kv')


class MultiSelectSpinner(Button):
    """Widget allowing to select multiple text options."""
    dropdown = ObjectProperty(None)
    """(internal) DropDown used with MultiSelectSpinner."""
    values = ListProperty([])
    """Values to choose from."""
    selected_values = ListProperty([])
    """List of values selected by the user."""
    def __init__(self, **kwargs):
        self.bind(dropdown=self.update_dropdown)
        self.bind(values=self.update_dropdown)
        super(MultiSelectSpinner, self).__init__(**kwargs)
        self.bind(on_release=self.toggle_dropdown)

    def toggle_dropdown(self, *args):
        if self.dropdown.parent:
            self.dropdown.dismiss()
        else:
            self.dropdown.open(self)

    def update_dropdown(self, *args):
        if not self.dropdown:
            self.dropdown = DropDown()
        values = self.values
        if values:
            if self.dropdown.children:
                self.dropdown.clear_widgets()
            for value in values:
                b = Factory.MultiSelectOption(text=value)
                b.bind(state=self.select_value)
                self.dropdown.add_widget(b)

    def select_value(self, instance, value):
        if value == 'down':
            # if instance.text not in self.selected_values:
            if instance.text == "del":
                if len(self.selected_values) > 0:
                    self.selected_values.pop()
            elif instance.text == "λ":
                self.selected_values = ["λ"]
            else:
                if len(self.selected_values) > 0 and self.selected_values[-1] == "λ":
                    self.selected_values.pop()
                self.selected_values.append(instance.text)
            App.get_running_app().root.get_screen("rules_sc").ids.i5.text = str(self.selected_values)[1:-1].replace(
                '\'', '').replace(' ', '')
        # else:
        #     if instance.text in self.selected_values:
        #         self.selected_values.remove(instance.text)

    def on_selected_values(self, instance, value):
        pass
        # if value:
        #     self.text = ', '.join(value)
        # else:
        #     self.text = ''


class State:
    def __init__(self, new_state: str, stack_pointer: list, stack_changes: list = ("λ",)):
        self.stack = [x for x in stack_pointer + (stack_changes[::-1] if stack_changes[0] != "λ" else [])]
        self.state = new_state

    def __str__(self):
        return f"{self.state!r} : {self.stack!r}"

    def __repr__(self):
        return str(self)


class MyManager(ScreenManager):
    states = ListProperty()
    alphabet = ListProperty()
    stack_alpha = ListProperty()
    starting = StringProperty()
    stack_base = StringProperty()
    accepted = ListProperty()
    rules = ListProperty()
    index = NumericProperty(0)

    @staticmethod
    def bg_color():
        return rgba("#B8860B")

    @staticmethod
    def button_color():
        return rgba(0, 0, 0)

    @staticmethod
    def button_fcolor():
        return rgba('#008080')

    @staticmethod
    def font_color():
        return rgba('#008080')  # '#50C878'

    def first(self, text1, text2, text3):
        if not (len(text1) == 1 and text1[0] == "") and not (len(text2) == 1 and text2[0] == "") and not (
                len(text3) == 1 and text3[0] == ""):
            self.states = text1
            self.alphabet = text2  # + ["λ"]
            self.stack_alpha = text3 + ["λ"]
            self.current = 'input2_sc'
            self.transition.direction = "left"

    def second(self, text1, text2, text3):
        if text1 in self.states and text2 in self.stack_alpha:
            t = True
            for i in text3:
                if i not in self.states:
                    t = False
                    break
            if t:
                self.starting = text1
                self.stack_base = text2
                self.accepted = text3
                self.current = 'rules_sc'
                self.transition.direction = "left"

    def fourth(self, text1, text2, text3, text4, text5):
        if text1 != "state" and text2 != "alpha" and text3 != "stack" and text4 != "state" and not (
                len(text5) == 1 and text5[0] == ""):
            t = True
            for i in text5:
                if i not in self.stack_alpha:
                    t = False
                    break
            if self.stack_base in text5[:-1]:
                t = False
            if t:
                self.rules.append({"from": text1, "with": text2, "while": text3, "to": text4, "new-stack": text5})
        # print(self.rules)

    def third(self):
        self.current = 'run_sc'
        self.transition.direction = "left"

    def check(self, to_check, scroll_obj):
        def print_q(Q: Queue):
            size_q = Q.qsize()
            for ii in range(size_q):
                temp = Q.get_nowait()
                print(temp, end="," if ii != size_q - 1 else "\n")
                Q.put_nowait(temp)

        if len(to_check.strip()) > 0:
            q = Queue()
            q.put(State(new_state=self.starting, stack_pointer=[self.stack_base]))
            text = f"processing input {self.index!s}:\n"
            self.index += 1
            for s in to_check:
                size = q.qsize()
                text += f"--->input character: {s} :\n"
                for i in range(size):
                    text += f"------->Queue update {i} :\n"
                    cur: State = q.get_nowait()
                    text += f"----------->current is : {cur!s}\n"
                    # scroll_obj.parent.text += str(cur) + "\n"
                    for r in self.rules:
                        if r['from'] == cur.state and r['with'] == s and r['while'] == cur.stack[-1]:
                            if not (r['new-stack'][-1] != self.stack_base and cur.stack[-1] == self.stack_base):
                                q.put(State(new_state=r['to'], stack_pointer=cur.stack[:-1],
                                            stack_changes=r['new-stack']))
                    # print_q(q)

            # scroll_obj.parent.text += "-----------------\n"
            accept = False
            while q.qsize() > 0:
                cur: State = q.get_nowait()
                if cur.state in self.accepted:
                    accept = True
                    break
            text += f"input acceptance : {accept!s}\n"
            # print(accept)
            text += "-" * 40 + ">ended.\n"
            scroll_obj.parent.text += text


class Screen1(Screen):
    text1 = ObjectProperty()
    text2 = ObjectProperty()
    text3 = ObjectProperty()


class Screen2(Screen):
    text1 = ObjectProperty()
    text2 = ObjectProperty()
    text3 = ObjectProperty()


class Screen3(Screen):
    pre_text = StringProperty()


class Screen4(Screen):
    pass


class MyScrollView(ScrollView):
    text = StringProperty("")


class MyApp(App):
    def build(self):
        my_window = MyManager()
        # my_window.current = "run_sc"
        return my_window


class Handler(ExceptionHandler):
    def handle_exception(self, inst):
        print(str(inst))
        return ExceptionManager.PASS


ExceptionManager.add_handler(Handler())

MyApp().run()
