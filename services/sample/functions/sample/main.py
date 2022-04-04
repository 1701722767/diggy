import json, yaml
class Request:
    """
    Request is the class used for handling the request
    """
    def __init__(self):
        self.err = None

    def process(self,message):
        print(message)



def lambda_handler(event, context):
    """
    lambda_handler function that starts the lambda
    """
    _ = context
    req = Request()
    try:
        req.process(event)

    except Exception as err:
        print(err)
    finally:
        if req.err is None:
            return "all is good siuuu"
        else:
            return "all is not good nouu"