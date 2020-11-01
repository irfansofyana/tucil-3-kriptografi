import tkinter as tk
import src.utils.gui as hg

from src.utils.file import write_file, get_file_size, get_abs_path

class EndPage(tk.Frame):
    def __init__(self, parent, controller, title, tipe, results):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        heading = tk.Label(
            self,
            bg="white",
            fg="black",
            text=title,
            font='none 20 bold'
        )
        heading.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        if (tipe == 'elgamal_key'):
            output_frame = hg.create_frame(self, 3)
            pub_key = results["public"]
            pri_key = results["private"]
            pub_output = results['public_name']
            pri_output = results['private_name']

            hg.create_label(output_frame, "Public Key (format: y g p)", 0, 0)
            public_key = f"{pub_key['y']} {pub_key['g']} {pub_key['p']}"
            hg.create_text(output_frame, public_key, 5, 70, 1, 0)
            hg.create_button(output_frame, 'Save Public Key!', lambda: self.save_key(True, pub_output, public_key), 6, 0)
            
            hg.create_label(output_frame, "Private Key (format: x p)", 7, 0)
            private_key = f"{pri_key['x']} {pri_key['p']}"
            hg.create_text(output_frame, private_key, 5, 70, 8, 0)
            hg.create_button(output_frame, 'Save Public Key!', lambda: self.save_key(False, pri_output, private_key), 9, 0)
        else:
            execution_time = results['execution_time']
            message = results['encrypted'] if ('encrypted' in results) else results['decrypted']
            file_output = results['file_output']

            output_frame = hg.create_frame(self, 3)
            if (file_output != ''):
                hg.create_label(output_frame, f"Saved to test-data/encrypted/{file_output}.txt!", 0, 0)
                hg.create_label(output_frame, f"Time execution is {execution_time}", 12, 0)
                abs_path = get_abs_path(f"test-data/encrypted/{file_output}.txt")
                file_size = get_file_size(abs_path)
                hg.create_label(output_frame, f"File size is {file_size}", 13, 0)
            else:
                hg.create_label(output_frame, "Encryption Result", 0, 0)
                hg.create_text(output_frame, message, 10, 70, 1, 0)
                hg.create_label(output_frame, f"Time execution is {execution_time}", 12, 0)
        
        back_frame = hg.create_frame(self, 6)
        hg.create_button(back_frame, 'Back', lambda: self.controller.show_frame("StartPage"), 0, 0)
    
    def save_key(self, is_public, filename, content):
        filename = "./test-data/keys/" + filename
        filename += '.pub' if (is_public) else '.pri'
        write_file(filename, content)