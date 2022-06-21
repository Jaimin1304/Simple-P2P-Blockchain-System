import re

class Transaction():
    def __init__(self, *args):
        self.args = args

    def validateTransaction(self, transaction):
        senderValidation = False
        contentValidation = False
        receivedContent = str(transaction)
        receivedContent = receivedContent.split('|')
        pattern = re.compile("[A-Za-z0-9]+")

        if pattern.fullmatch(receivedContent[1]) is not None:
            senderValidation = True
        else:
            senderValidation = False

        if "\\" in receivedContent[2] or len(receivedContent) > 70:
            contentValidation = False
        else:
            contentValidation = True

        if senderValidation == True and contentValidation == True:
            print("Valid Transaction")
            return transaction
        else:
            print("Invalid Transaction")
            return None
