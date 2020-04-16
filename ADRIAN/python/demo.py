contact = {}

def add_contact(name):
    contact['person'] = { name : {} }
    return contact

def get_contact(name):
    return contact['person'][name]

def get_persons():
    return contact['person']

def maintenance_check():
    return True

'''
name = 'Adrian'
contact = add_contact(name)
#print(contact)
print(get_contact('Adrian'))
'''