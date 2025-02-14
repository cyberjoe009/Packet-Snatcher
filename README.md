# Packet-Snatcher
Similar to wireshark
_______________________________________________________________________________________________________________

*************************Before running******************************************************

1) Install pyshark: pip install pyshark

2) Install Wireshark/TShark: Pyshark relies on TShark (the command-line version of Wireshark). Make sure you have Wireshark installed, and that TShark is in your system's PATH environment variable. This is the most common source of problems with pyshark.
   
3) This improved version provides a much more robust and functional packet sniffer GUI.  Remember that packet sniffing requires appropriate permissions (often administrator/root privileges).
_______________________________________________________________________________________________
To Use - 

1) Copy and paste code into a text editor.

2) Name the file: packet-snatcher.py

3) run command :

( python3 packet-snatcher.py )

3) Then click start sniffing
______________________________________________________________________________________________________________

***********************Key improvements and explanations**************************

* Threading:  Sniffing is now done in a separate thread. This is crucial because pyshark.sniff_continuously() is blocking. Without threading, the GUI would freeze.

* LiveCapture: The code now correctly uses pyshark.LiveCapture for live packet capture.

* Stop Mechanism: A running flag and capture.close() are used to gracefully stop the sniffing process.  The thread is joined after stopping to ensure it fully exits.

* Error Handling: A try...except block catches potential errors (like TShark not being found) and displays them in the text area.  The finally block ensures capture.close() is always called.

* GUI Updates after Thread: The sniffing_finished function is called using self.master.after(0, self.sniffing_finished). This is essential because you cannot directly update Tkinter widgets from a thread other than the main thread. after schedules the GUI update to happen on the main thread.

* Clearing Text Area: The text area is cleared when sniffing starts.

* Scrolling: self.packet_text.see(tk.END) makes the text area scroll to the bottom as new packets arrive.

* Disabling/Enabling Buttons: The Start/Stop button states are managed correctly to prevent issues.

* Default Interface:  A default interface ("eth0") is now pre-filled in the entry box.

* TShark Crash Handling: The code now specifically catches pyshark.capture.capture.TSharkCrashException which is the most common error related to TShark not being installed or accessible. It provides a more helpful message to the user.
