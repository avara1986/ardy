def my_handler(event, context):
    message = 'Hello world lambda1! This is a new version 3'
    return {
        'message': message
    }
