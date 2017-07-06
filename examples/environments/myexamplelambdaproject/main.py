def my_handler(event, context):
    message = 'Hello world lambda isolated!' 
    return { 
        'message' : message
    }   
