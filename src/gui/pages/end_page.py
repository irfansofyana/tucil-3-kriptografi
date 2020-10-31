import tkinter as tk
import src.utils.gui as hg

from src.utils.file import write_file

class EndPage(tk.Frame):
    def __init__(self, parent, controller, title, tipe, results):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        heading = tk.Label(
            self,
            bg="white",
            fg="black",
            text=title,
            font='none 24 bold'
        )
        heading.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        if (tipe == 'elgamal_key'):
            output_frame = hg.create_frame(self, 2)
            pub_key = results["public_key"]
            pri_key = results["private_key"]
            pub_output = results['public_name']
            pri_output = results['private_name']

            hg.create_label(output_frame, "Public Key (format: y g p)", 0, 0)
            public_key = f"{pub_key['y']} {pub_key['g']} {pub_key['p']}"
            hg.create_label(output_frame, public_key, 1, 0)
            hg.create_button(output_frame, 'Save Public Key!', lambda: self.save_key(True, pub_output, public_key), 1, 1)
            
            hg.create_label(output_frame, "Private Key (format: x p)", 2, 0)
            private_key = f"{pri_key['x']} {pri_key['p']}"
            hg.create_label(output_frame, private_key, 3, 0)
            hg.create_button(output_frame, 'Save Public Key!', lambda: self.save_key(False, pri_output, private_key), 3, 1)
        elif:
            execution_time = results['execution_time']
            message = results['encrypted'] if ('encrypted' in results) else results['decrypted']
            file_output = results['file_output']

            output_frame = hg.create_frame(self, 2)
            if (file_output != ''):
                hg.create_label(output_frame, f"Saved to file {file_output}!", 0, 0)
            else:
                hg.create_label(output_frame, message, 0, 0)
            
            hg.create_label(output_frame, f"Time execution is {execution_time}", 1, 0)
            hg.create_label(output_frame, f"File size is ...", 2, 0)
        
        
        back_frame = hg.create_frame(self, 10)
        hg.create_button(back_frame, 'Back', lambda: self.controller.show_frame("StartPage"), 0, 1)
    
    def save_key(self, is_public, filename, content):
        filename += '.pub' if (is_public) else '.pri'
        write_file(filename, content)