from tkinter import *
from tkinter import ttk
import requests
import json

# Initialize window
window = Tk()
window.title("Ryu QoS")
window.geometry('350x400')

tab_control = ttk.Notebook(window)
 
tab1 = Frame(tab_control)

tab_control.add(tab1, text = "QoS")

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

txt = []
labels = []

txt_queue = []
lbl_queue = []

# Adds buttons and labels to the first frame

for i in range(len(fields_list)):
    labels.append(Label(tab1, text = fields_list[i]))
    labels[i].grid(column = 0, row = (i + 2), padx = (10, 10), pady = (2, 2), sticky = E)
    if i != 5 or i != 8:
        txt.append(Entry(tab1, width = 16))
        txt[i].grid(column = 1, row = (i + 2), padx = (10, 10), pady = (2, 2), sticky = W)

dl_type = ttk.Combobox(tab1)
dl_type['values'] = ("ARP", "IPV4", "")
dl_type.current(1)
dl_type.grid(column = 1, row = 7)

nw_proto = ttk.Combobox(tab1)
nw_proto['values'] = ("TCP", "UDP", "ICMP", "")
nw_proto.current(1)
nw_proto.grid(column = 1, row = 10)

actions = ttk.Combobox(tab1)
actions['values'] = ("mark", "meter", "queue")
actions.current(1)
actions.grid(column = 1, row = 14)

# Label will be implemented alongside the button
lbl_status = Label(tab1, text = "")
lbl_status.grid(column = 1, row = 16, padx = (10, 10), pady = (2, 2), sticky = E)

action_values = Entry(tab1, width = 16)
action_values.grid(column = 1, row = 15, padx = (10, 10), pady = (2, 2), sticky = W)

def clicked():
    syntax = []
    lbl_status.configure(text = "")
    # Ensure that the essential information is inserted
    
    if len(txt[1].get()) != 0:
        syntax.append("\"priority\": " + "\"" + txt[1].get() + "\"")
    if len(txt[2].get()) != 0:
        syntax.append("\"in_port\": " + "\"" + txt[2].get() + "\"")        
    if len(txt[3].get()) != 0:
        syntax.append("\"dl_src\": " + "\"" + txt[3].get() + "\"")
    if len(txt[4].get()) != 0:
        syntax.append("\"dl_dst\": " + "\"" + txt[4].get() + "\"")
    if dl_type.get() != "":
        syntax.append("\"dl_type\": " + "\"" + dl_type.get() + "\"")
    if len(txt[6].get()) != 0:
        syntax.append("\"nw_src\": " + "\"" + txt[6].get() + "\"")
    if len(txt[7].get()) != 0:
        syntax.append("\"nw_dst\": " + "\"" + txt[7].get() + "\"")
    if nw_proto.get() != "":
        syntax.append("\"nw_type\": " + "\"" + nw_proto.get() + "\"")
    if len(txt[9].get()) != 0:
        syntax.append("\"tp_src\": " + "\"" + txt[9].get() + "\"")
    if len(txt[10].get()) != 0:
        syntax.append("\"tp_dst\": " + "\"" + txt[10].get() + "\"")
    if len(txt[11].get()) != 0:
        syntax.append("\"ip_dscp\": " + "\"" + txt[11].get() + "\"")
    if len(action_values.get()) != 0:
        syntax.append("\"ip_dscp\": " + "\"" + txt[11].get() + "\"")
            
    dpid = txt[0].get()
    req = "http://localhost:8080/qos/rules/" + dpid

    match = '{"match": {'

    syntax_len = len(syntax) - 1
    
    for i in range(len(syntax)):
        if i == syntax_len:
            match += syntax[i]
        else:
            match += syntax[i] + ", "
        
    match += '}, "actions":{' + "\"" + actions.get() + "\"" + ": " + "\"" + action_values.get() + "\"}}"

    status = None

    try:
        status = requests.post(req, match)
    except Exception:
        lbl_status.configure(text = "Connection Error")
    

    print(status)
    print(type(status))
    """
    if "200" in status:
        lbl_status.configure("Success")
    else:
        lbl_status.configure("Failed")
    """
btn = Button(tab1, text = "Apply", command = clicked)
btn.grid(column = 0, row = 16, padx = (10, 10), pady = (2, 2), sticky = E)

tab_control.pack(expand = 1, fill = 'both')

# Makes GUI appear
window.mainloop()
