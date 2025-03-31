import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext
from PIL import Image, ImageTk
from utils.logging import log
from utils.llm import get_llm_response


class NegotiationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Negotiation Simulation")
        self.round_number = 1
        self.opponent = [[2, 3, 2], [2, 3, 3], [2, 4, 3], [3, 4, 3], [3, 4, 4], [4, 4, 4]]
        self.user_id = ""

        self.start_screen()

    def start_screen(self):
        self.clear_screen()
        label = tk.Label(self.root, text="Enter Your ID to Start", font=("Arial", 14))
        label.pack(pady=10)
        self.id_entry = tk.Entry(self.root)
        self.id_entry.pack(pady=5)
        start_button = tk.Button(self.root, text="Start Simulation", command=self.save_id)
        start_button.pack(pady=10)

    def save_id(self):
        self.user_id = self.id_entry.get().strip()
        if not self.user_id:
            messagebox.showwarning("Warning", "Please enter a valid ID")
            return
        log(f"User ID: {self.user_id}", self.user_id)
        self.main_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def main_screen(self):
        self.clear_screen()

        image = Image.open("john.jpg")
        image = image.resize((80, 80))
        self.photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(self.root, image=self.photo)
        image_label.pack(pady=5)

        title = tk.Label(self.root, text=f"Negotiation with John", font=("Arial", 14))
        title.pack(pady=5)

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.left_text = scrolledtext.ScrolledText(self.frame, width=40, height=20, font=("Arial", 10), wrap=tk.WORD)
        self.left_text.grid(row=0, column=0, padx=5)

        self.right_text = scrolledtext.ScrolledText(self.frame, width=40, height=20, font=("Arial", 10), wrap=tk.WORD)
        self.right_text.grid(row=0, column=1, padx=5)

        self.accept_button = tk.Button(self.root, text="Accept Offer", command=self.accept_offer, width=20, bg="lightgreen")
        self.accept_button.pack(pady=5)

        self.counter_button = tk.Button(self.root, text="Counter Offer", command=self.counter_offer, width=20, bg="lightblue")
        self.counter_button.pack(pady=5)

        self.next_round()

    def next_round(self):
        if self.round_number > 6:
            self.left_text.insert(tk.END, "\nFinal Round reached. Negotiation ended.\n")
            log("Negotiation Ended: Final round without agreement.", self.user_id)
            self.summary()
            self.disable_buttons()
            return

        self.current_offer = self.opponent[self.round_number - 1]
        text = f"\n Round {self.round_number} - Opponent Offer: \nPrice-{self.current_offer[0]}, Waranty-{self.current_offer[1]}, number three-{self.current_offer[2]}\n"
        self.left_text.insert(tk.END, text)
        log(text.strip(), self.user_id)

    def accept_offer(self):
        text = "You accepted the offer.\n"
        self.left_text.insert(tk.END, text)
        log("User Response: accept", self.user_id)
        self.summary()
        messagebox.showinfo("Negotiation Finished", "You've accepted the offer.")
        self.disable_buttons()

    def counter_offer(self):
        log("User Response: counter-offer", self.user_id)

        while True:
            question = simpledialog.askstring("Agent Help", "Ask your question (type 'finish' to stop):")
            if not question or question.lower() == "finish":
                break
            log(f"User Question to Agent: {question}", self.user_id)
            self.right_text.insert(tk.END, f"\nUser: {question}\n")
            response = get_llm_response(question)
            self.right_text.insert(tk.END, f"\nAgent: {response}\n")
            log(f"Agent Response: {response}", self.user_id)

        user_offer = simpledialog.askstring("Counter Offer", "Enter your offer (e.g., 3,4,2):")
        if user_offer:
            log(f"User Counter Offer: {user_offer}", self.user_id)
            self.left_text.insert(tk.END, f"\n You proposed a counter offer: {user_offer}\n")

        self.round_number += 1
        self.next_round()

    def summary(self):
        with open(f'negotiation_log_{self.user_id}.txt', encoding='utf-8') as f:
            log_text = f.read()

        prompt = f"""
Summary of negotiation:
- User ID: {self.user_id}
- Total Rounds: {min(self.round_number, 6)}
- Final Opponent Offer: {self.current_offer}
- Final User Response: {'accept' if 'accept' in log_text else 'no agreement'}
How can I do better?
"""
        response = get_llm_response(prompt)
        self.right_text.insert(tk.END, f"\n[Negotiation Summary]\n{response}\n")
        log(f"Summary:\n{response}", self.user_id)

    def disable_buttons(self):
        self.accept_button.config(state=tk.DISABLED)
        self.counter_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = NegotiationApp(root)
    root.mainloop()
