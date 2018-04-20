#function to convert US Dollar to Indian Ruppees
def inr(usd):
    return(usd*64.52)
#Function to convert Indian Ruppees to US Dollar
def usd(inr):
    return(inr/64.52)

choice="y"
while (choice=="y" or choice=="Y"):
    print("\n\n")
    print('_'*5,"CURRENCY CONVERTER",'_'*5,"\n")
    print("1. US Dollar To INR")            
    print("2. INR To US Dollar")
    ch=int(input("\nENTER YOUR CHOICE (1/2) : "))       #Taking choice as input from user 
    if ch==1:
        amount=int(input("\nEnter The Amount In USD :: "))
        print("Amount In INR :: ",inr(amount))
    
    elif ch==2:
        amount=int(input("\nEnter The Amount In INR :: "))
        print("Amount In INR :: ",usd(amount))

    else:
        print("Invalid Choice ! ")

    choice= input("\n Do You Wanna Continue :: ")
        







