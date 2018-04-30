from tkinter import *

# Initialize window
window = Tk()
window.title("Ryu QoS")
window.geometry('350x400')

fields_list = ["Datapath ID:",          # 0
               "Ethernet Source",       # 1
               "Ethernet Destination",  # 2
               "Ethernet Type",         # 3
               "IP Source",             # 4
               "IP Destination",        # 5
               "IP Protocol",           # 6
               "Port Source",           # 7
               "Port Destination",      # 8
               "IP DSCP"                # 9
               ]
txt = []
labels = []

for i in range(len(fields_list)):
    # print(i)
    labels.append(Label(window, text = fields_list[i]))
    labels[i].grid(column = 0, row = i)
    txt.append(Entry(window, width = 10))
    txt[i].grid(column = 1, row = i)

# Label will be implemented alongside the button
lbl_status = Label(window, text = "")
lbl_status.grid(column = 1, row = 12)

def clicked():
    syntax = []
    items = ""

    if len(txt[0].get()) == 0:
        lbl_status = "Please add a valid DPID"
        return

    if len(txt[1].get()) != 0:
        syntax.append("\"dl_src\": " + "\"" + txt[1].get() + "\"")
        print(items)

    optional_nums = [1, 6, 7, 8]

    # for i in range(len(fields_list)):

    dpid = txt[0].get()
    req = "http://localhost:8080/qos/queue/" + dpid
    lbl_status.configure(text = req)

btn = Button(window, text = "Apply", command = clicked)
btn.grid(column = 0, row = 12)

# Makes GUI appear
window.mainloop()
