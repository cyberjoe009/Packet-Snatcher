import tkinter as tk
from tkinter import scrolledtext
import pyshark
import threading

class PacketSnifferGUI:
    def __init__(self, master):
        self.master = master
        master.title("Simple Packet Sniffer")

        self.interface_label = tk.Label(master, text="Interface:")
        self.interface_label.grid(row=0, column=0, sticky="w")

        self.interface_entry = tk.Entry(master)
        self.interface_entry.insert(0, "eth0")  # Default interface
        self.interface_entry.grid(row=0, column=1, sticky="ew")

        self.start_button = tk.Button(master, text="Start Sniffing", command=self.start_sniffing)
        self.start_button.grid(row=1, column=0, columnspan=2)

        self.stop_button = tk.Button(master, text="Stop Sniffing", command=self.stop_sniffing, state=tk.DISABLED)
        self.stop_button.grid(row=2, column=0, columnspan=2)


        self.packet_text = scrolledtext.ScrolledText(master, wrap=tk.WORD)
        self.packet_text.grid(row=3, column=0, columnspan=2, sticky="nsew")
        self.packet_text.config(state=tk.DISABLED)  # Initially disable text area

        self.capture = None  # pyshark capture object
        self.running = False  # Flag to control sniffing thread

    def start_sniffing(self):
        interface = self.interface_entry.get()
        if not interface:
            self.packet_text.config(state=tk.NORMAL)
            self.packet_text.insert(tk.END, "Please enter a valid interface.\n")
            self.packet_text.config(state=tk.DISABLED)
            return

        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.packet_text.config(state=tk.NORMAL)
        self.packet_text.delete(1.0, tk.END)  # Clear previous packets
        self.running = True

        self.sniffing_thread = threading.Thread(target=self.sniff_packets, args=(interface,))
        self.sniffing_thread.start()

    def sniff_packets(self, interface):
        try:
            self.capture = pyshark.LiveCapture(interface=interface) # Using LiveCapture for live sniffing
            for packet in self.capture.sniff_continuously():  # Sniff until stopped
                if not self.running:  # Check stop flag
                    break

                packet_str = str(packet)  # Or format it more nicely
                self.packet_text.insert(tk.END, packet_str + "\n\n")
                self.packet_text.see(tk.END) # Scroll to the bottom
        except pyshark.capture.capture.TSharkCrashException as e:
            self.packet_text.insert(tk.END, f"TShark Error: {e}\nEnsure Wireshark/TShark is installed and in your PATH.\n")
        except Exception as e:
            self.packet_text.insert(tk.END, f"Error: {e}\n")
        finally:
            self.capture.close() # Important: Close the capture!
            self.running = False
            self.master.after(0, self.sniffing_finished) # Use after to update GUI

    def sniffing_finished(self):
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.packet_text.config(state=tk.DISABLED)

    def stop_sniffing(self):
        self.running = False  # Set flag to stop the loop
        if self.capture:
            self.capture.close() # Close capture if it exists (might not if an error occurred early)
        self.sniffing_thread.join() # Wait for the thread to actually stop
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.packet_text.config(state=tk.DISABLED)


root = tk.Tk()
sniffer_gui = PacketSnifferGUI(root)
root.mainloop()
