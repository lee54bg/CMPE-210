from tkinter import *
from tkinter import ttk

# Initialize window
window = Tk()
window.title("Ryu QoS")
window.geometry('350x400')

tab_control = ttk.Notebook(window)
 
tab1 = Frame(tab_control)
tab2 = Frame(tab_control)

tab_control.add(tab1, text = "QoS")
tab_control.add(tab2, text = "Queue")

fields_list = ["Datapath ID",           # 0
               "Priority",              # 1
               "IN_PORT",               # 2
               "Ethernet Source",       # 3
               "Ethernet Destination",  # 4
               "Ethernet Type",         # 5
               "IP Source",             # 6
               "IP Destination",        # 7
               "IP Protocol",           # 8
               "Port Source",           # 9
               "Port Destination",      # 10
               "IP DSCP"                # 11
               ]

queue_list = ["Datapath ID",           # 0
              "Port Name",             # 1
              "Type",                  # 2
              "Max rate",              # 3
              "Queue Max rate",        # 4
              "Queue Min rate"         # 5
              ]

txt = []
labels = []

txt_queue = []
lbl_queue = []

# Adds buttons and labels to the first frame

for i in range(len(fields_list)):
    labels.append(Label(tab1, text = fields_list[i]))
    labels[i].grid(column = 0, row = (i + 2), padx = (10, 10), pady = (2, 2), sticky = E)
    txt.append(Entry(tab1, width = 16))
    if i != 5 or i != 8:
        txt[i].grid(column = 1, row = (i + 2), padx = (10, 10), pady = (2, 2), sticky = W)

dl_type = ttk.Combobox(tab1)
dl_type['values'] = ("ARP", "IPV4")
dl_type.current(1)
dl_type.grid(column = 1, row = 5)

nw_proto = ttk.Combobox(tab1)
nw_proto['values'] = ("TCP", "UDP", "ICMP")
nw_proto.current(1)
nw_proto.grid(column = 1, row = 8)

actions = ttk.Combobox(tab1)
actions['values'] = (1, 2, 3, 4, 5)
actions.current(1)
actions.grid(column = 1, row = 13)

# Adds buttons and labels to the second frame

for i in range(len(queue_list)):
    lbl_queue.append(Label(tab2, text = queue_list[i]))
    lbl_queue[i].grid(column = 0, row = (i + 2), padx = (10, 10), pady = (2, 10), sticky = E)
    txt_queue.append(Entry(tab2, width = 16))
    txt_queue[i].grid(column = 1, row = (i + 2), padx = (10, 10), pady = (2, 2))

# Label will be implemented alongside the button
lbl_status = Label(tab1, text = "")
lbl_status.grid(column = 1, row = 14, padx = (10, 10), pady = (2, 2), sticky = E)

def clicked():
    syntax = []
    items = ""

    # Ensure that the essential information is inserted
    if len(txt[0].get()) == 0:
        lbl_status.configure(text = "Please add a valid DPID")
        return
    if len(txt[3].get()) == 0:
        lbl_status.configure(text = "Please add a valid Ethernet Source")
        return
    if len(txt[4].get()) == 0:
        lbl_status.configure(text = "Please add a valid Ethernet Destination")
        return
    if len(txt[6].get()) == 0:
        lbl_status.configure(text = "Please add a valid IP Source")
        return
    if len(txt[7].get()) == 0:
        lbl_status.configure(text = "Please add a valid IP Destination")
        return
    
    if len(txt[1].get()) != 0:
        syntax.append("\"priority\": " + "\"" + txt[1].get() + "\"")
    if len(txt[3].get()) != 0:
        syntax.append("\"dl_src\": " + "\"" + txt[3].get() + "\"")
    if len(txt[4].get()) != 0:
        syntax.append("\"dl_dst\": " + "\"" + txt[4].get() + "\"")
    if len(txt[6].get()) != 0:
        syntax.append("\"nw_src\": " + "\"" + txt[6].get() + "\"")
    if len(txt[7].get()) != 0:
        syntax.append("\"nw_dst\": " + "\"" + txt[7].get() + "\"")
    if len(txt[9].get()) != 0:
        syntax.append("\"tp_src\": " + "\"" + txt[9].get() + "\"")
    if len(txt[10].get()) != 0:
        syntax.append("\"tp_dst\": " + "\"" + txt[10].get() + "\"")
    if len(txt[11].get()) != 0:
        syntax.append("\"ip_dscp\": " + "\"" + txt[11].get() + "\"")
        
    req_nums = [1, 6, 7, 8]

    dpid = txt[0].get()
    req = "http://localhost:8080/qos/queue/" + dpid
    lbl_status.configure(text = req)

# Button for frame 1

btn = Button(tab1, text = "Apply", command = clicked)
btn.grid(column = 0, row = 14, padx = (10, 10), pady = (2, 2), sticky = E)

tab_control.pack(expand = 1, fill = 'both')

# Makes GUI appear
window.mainloop()
