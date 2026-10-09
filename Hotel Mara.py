import csv
#flaws quantity 0,customer login,
s=[]
f1=open('Menu.csv','w+',newline='')
a=csv.writer(f1)
a.writerow(['Item Name','Price','Description','Cuisine'])
z=[
  ["Balsamic Glazed Lamb Chops",300,'Succulent lamb chops seared to perfection and coated in a tangy-sweet balsamic glaze with hints of garlic, honey, and rosemary for a rich, flavorful finish.','Hotel Sunshine Special'],
  ["Mango Tango Shrimp Tacos",250,"Juicy shrimp infused with tropical mango salsa, nestled in warm tortillas, creating a vibrant explosion of flavors that dance on your palate with every bite.",'Hotel Sunshine Special'],
  ["Garden Delight Stir-Fry",150,"A vibrant medley of fresh vegetables stir-fried to perfection, seasoned with aromatic spices for a burst of flavor.",'Hotel Sunshine Special'],
  ["Savory Spinach and Ricotta Ravioli",160,"Handmade ravioli stuffed with creamy ricotta cheese and spinach, served in a light herb-infused sauce.",'Hotel Sunshine Special'],
  ["Dreamy Chocolate Avalanche",250,"Layers of indulgent chocolate bliss, topped with edible gold.",'Hotel Sunshine Special'],
  ["Blissful Berry Symphony",270,"A harmonious medley of fresh berries layered atop delicate sponge cake, drizzled with a luscious berry reduction and crowned with a dollop of whipped cream.",'Hotel Sunshine Special'],
  ["Chicken 65",110,'Spicy, crispy fried chicken tossed with chilies, garlic, and aromatic spices for a bold, flavorful kick.','Starters'],
  ["Chicken wings",120,"Juicy chicken wings, drenched and marinated, then deep-fried to perfection, offering a crispy and flavorful appetizer.",'Starters'],
  ["Chicken Tikka",150,"Tender pieces of marinated chicken grilled to perfection, bursting with smoky and aromatic flavors.",'Starters'],
  ["Veg Crispy",100,"Crispy and flavorful deep-fried vegetables coated in a crunchy batter, perfect as a crunchy appetizer.",'Starters'],
  ["Mushroom n pepper fry",110,"Sautéed mushrooms and peppers seasoned with aromatic spices, offering a flavorful and savory dish.",'Starters'],
  ["Paneer Chilli",120,"Cubes of paneer tossed in a spicy and tangy sauce with peppers and onions, offering a delicious and flavorful Indo-Chinese dish.",'Starters'],
  ["Idli",60,"Two idilis along with sambar and coconut chutney",'South Indian'],
  ["Masala Dosa",80,"Two masala dosas overloaded with potato filling along with chutney",'South Indian'],
  ["Uttapam",100,"Two uttapam with veggies on top along with tomato chutney.",'South Indian'],
  ["Medu Vada",80,"4 medu vada along with sambar and coconut chutney",'South Indian'],
  ["Parotta with Mutton Curry",160,"Four parotas with spicy mutton curry made from blend of spices and tender mutton pieces.",'South Indian'],
  ["Chinese Bhel",30,"crispy noodles, colorful veggies, and tangy sauces, offering a unique twist on traditional Indian street food.",'Chinese Ching'],
  ["Momos",70,"Savory dumplings filled with seasoned vegetable, steamed to perfection and served with a side of spicy dipping sauce.",'Chinese Ching'],
  ["Schezwan Fried Rice",180,"A fiery blend of rice, vegetables, and spicy Schezwan sauce, wok-fried to perfection for a tantalizing flavorful experience.",'Chinese Ching'],
  ["Hakka Noodles",90,"Stir-fried noodles tossed with crispy vegetables and savory sauces, delivering a delightful fusion of flavors in every bite.",'Chinese Ching'],
  ["Manchurian Gravy",120," A savory and tangy Chinese-style sauce enveloping fried vegetable balls, offering a burst of flavor with every spoonful.",'Chinese Ching'],
  ["Palak Paneer",150,"Creamy spinach curry with chunks of soft paneer, infused with aromatic spices for a delicious vegetarian delight.",'Vegetarian Verna'],
  ["Paneer Tikka Masala",120,"Tender paneer cubes grilled to perfection and simmered in a rich, creamy tomato-based masala sauce, bursting with aromatic spices.",'Vegetarian Verna'],
  ["Mutter Paneer",110,"A comforting dish featuring soft paneer cubes and tender peas cooked in a flavorful tomato-based gravy, seasoned with aromatic spices.",'Vegetarian Verna'],
  ["Dal Tadka",100,"Creamy lentils tempered with aromatic spices, offering a comforting and flavorful Indian staple.",'Vegetarian Verna'],
  ["Veg Biryani",130,"Fragrant basmati rice cooked with an assortment of vegetables and aromatic spices, creating a flavorful and satisfying one-pot meal.",'Vegetarian Verna'],
  ["Butter Chicken",150,"Tender chicken pieces simmered in a creamy, tomato-based sauce, infused with rich spices for a decadent and flavorful dish.",'Non-Vegetarian Delicacies'],
  ["Mutton Handi",180,"Succulent pieces of mutton cooked in a rich and aromatic gravy, simmered to perfection in a traditional clay pot.",'Non-Vegetarian Delicacies'],
  ["Nalli Nihari",190,"Tender lamb shanks slow-cooked in a flavorful gravy, infused with aromatic spices for a melt-in-your-mouth experience.",'Non-Vegetarian Delicacies'],
  ["Chicken Biryani",200,"Fragrant basmati rice cooked with succulent chicken pieces and aromatic spices, creating a flavorful.",'Non-vegetarian Delicacies'],
  ["Gulab Jamun",60,"Soft and syrupy milk-based balls infused with cardamom, rose water, and saffron, offering a sweet and indulgent treat",'Desserts and Beverages'],
  ["Ras Malai",80,"Soft and creamy cheese dumplings soaked in sweetened, flavored milk, garnished with nuts for a delightful dessert experience",'Desserts and Beverages'],
  ["Jalebi",50,"Crispy, deep-fried swirls of dough soaked in sugary syrup, offering a sweet and indulgent treat with a hint of tanginess.",'Desserts and Beverages'],
  ["Citrus Splash",120,"A refreshing blend of citrus fruits, bursting with tangy and zesty flavors, perfect for quenching your thirst on a hot day.",'Desserts and Beverages'],
  ["Mango Mania",140,"A tropical explosion of ripe mangoes, delivering a sweet and juicy burst of flavor in every bite.",'Desserts and Beverages'],
  ["Berry Blast Elixir",160," A vibrant fusion of assorted berries, creating a refreshing and invigorating drink bursting with antioxidants and natural sweetness.",'Desserts and Beverages'],
  ["Roti",10,"Traditional Indian flatbread, perfectly baked to be soft and fluffy.",'Add Ons'],
  ["Kulcha",15,"Soft, leavened bread, often served with a variety of dishes, including curries and dals.",'Add Ons'],
  ["Butter Naan",15,"A rich and soft flatbread brushed with butter, perfect for scooping up flavorful curries.",'Add Ons'],
  ["Garlic Butter Naan",18,"Delicious naan infused with garlic and a touch of butter, adding an extra layer of flavor.",'Add Ons'],
  ["Rumali Roti",15,"Thin and soft Indian bread, known for its light texture and perfect for wrapping up food.",'Add Ons'],
  ["Parotta",18,"Flaky and layered bread, known for its crispy texture and versatility with various dishes.",'Add Ons'],]

a.writerows(z)
f1.close()

#function for adding items in our menu
def ADDITEMS():
    f1=open('Menu.csv','a+',newline='')
    a=csv.writer(f1)
    b=csv.reader(f1)
    try:
        x=eval(input('Enter the new item in form of [Item Name,Price,Description,Cuisine] :'))
        for i in b:
            if i[0]==x[0]:
                print('''This item already exists:
                      Please add a new item
                                or          
                      Use the Update function''')
                f1.close()      
                return None
        if type(x)==list and len(x)==4 and type(x[0])==str and type(x[1])==int and type(x[2])==str and type(x[3])==str:
            a.writerow(x)
            print('Item sucessfully added')
        else:
            print('''Please ensure the following:
                  1.Item Name is given as string
                  2.Price is given as integer
                  3.Description is given as string
                  4.Cuisine is given as string''')
    except(NameError,SyntaxError):
        print('Please ensure everything added is correct')
    f1.close()
   
   
#update item present in menu    
def UPDATEITEMS():
    f1=open('Menu.csv','r')
    a=csv.reader(f1)
    count=0
    updatedlist=[]
    try:
        x=input('Enter the Item Name of the item you want to change :')
        for i in a:
            if i[0]==x:
                count+=1
                print(count)
            else:
                updatedlist.append(i)  
        if count==0:
            print('No such item exists')
            f1.close()
            return None
    except(NameError,SyntaxError,TypeError):
        print('Please ensure everything entered is correct')
        updatedlist.clear()
        f1.close()
        return None
    f1.close()
    f1=open('Menu.csv','a+',newline='')
    b=csv.writer(f1)
    try:
          y=eval(input('Enter the Updated Item in form of [Item Name,Price,Description,Cuisine] :'))
          if type(y)==list and len(y)==4 and type(y[0])==str and type(y[1])==int and type(y[2])==str and type(y[3])==str:
              updatedlist.append(y)
              b.writerows(updatedlist)
              print('Updated succesfully')
          else:
              print('''Please ensure the following:
            1.Item Name is given as string
            2.Price is given as integer
            3.Description is given as string
            4.Cuisine is given as string''')
    except(NameError,SyntaxError):
        print('Please ensure everything entered is correct')
    f1.close()
# ADDITEMS()      
#UPDATEITEMS()    


#DELETE_AND_SAVE_RECORD('Menu.csv', 'DeletedRecords.csv')
def DELETE_AND_SAVE_RECORD(source_file, deleted_file):
    try:

        file= open(source_file, 'r', newline='')
        reader = csv.reader(file)
        records = list(reader)

        item_to_delete = input('Enter the name of the item you want to delete: ')
        deleted_record = None

        updated_records = []
        for record in records:
            if record[0].strip() == item_to_delete.strip():
                deleted_record = record
            else:
                updated_records.append(record)

        if not deleted_record:
            print('No item such item found')
            return

        file=open(source_file, 'w', newline='')
        writer = csv.writer(file)
        writer.writerows(updated_records)


        file=open(deleted_file, 'a', newline='')
        writer = csv.writer(file)
        writer.writerow(deleted_record)

        print('Item ',item_to_delete,' was deleted and saved in' ,deleted_file,'.')


    except:
        print("An error occurred")


#Display
def DISPLAY():
    f1=open('Menu.csv','r')
    ok=csv.reader(f1)
    for i in ok:
        print('Item Name :',i[0])
        print('Price(₹) :',i[1])
        print('Description :',i[2])
        print('Cuisine :',i[3])
        print('\n')
    print('\n')
    print('Thank You')
    f1.close()
# DISPLAY()        


def MENUDISPLAY(ab):
    f1=open('Menu.csv','r')
    str(ab)
    b=csv.reader(f1)
    if ab==1:
        for i in b:
            if str(i[3])=='Starters':
                print('Item Name :',i[0])
                print('Price(₹) :',i[1])
                print(i[2])
                print('\n')
        ORDER()
               
    if ab==2:
        for i in b:
            if i[3]=='South Indian':
                print('Item Name :',i[0])
                print('Price(₹) :',i[1])
                print(i[2])
                print('\n')
        ORDER()
    if ab==3:
        for i in b:
            if i[3]=='Chinese Ching':
                print('Item Name :',i[0])
                print('Price(₹) :',i[1])
                print(i[2])
                print('\n')
        ORDER()        
    if ab==4:
        for i in b:
            if i[3]=='Vegetarian Verna':
                print('Item Name :',i[0])
                print('Price(₹) :',i[1])
                print(i[2])
                print('\n')
        ORDER()      
    if ab==5:
        for i in b:
            if i[3]=='Non Vegetarian Delicacies':
                print('Item Name :',i[0])
                print('Price(₹) :',i[1])
                print(i[2])
                print('\n')
        ORDER()        
    if ab==6:
        for i in b:
            if i[3]=='Hotel Sunshine Special':
                print('Item Name :',i[0])
                print('Price(₹) :',i[1])
                print(i[2])
                print('\n')
        ORDER()        
    if ab==7:
        for i in b:
            if i[3]=='Desserts and Beverages':
                print('Item Name :',i[0])
                print('Price(₹) :',i[1])
                print(i[2])
                print('\n')
        ORDER()
    if ab==8:
        for i in b:
            if i[3]=='Add Ons':
                print('Item Name :',i[0])
                print('Price(₹) :',i[1])
                print(i[2])
                print('\n')
        ORDER()    
    f1.close()          
               
                 
#bill order list
def ORDER():
    f1=open('Menu.csv','r')
    global s
    b=csv.reader(f1)
    count=0
    while True:
        try:
           q=input('Enter the name of item as it is given :')
           qe=int(input('Enter quantity :'))
           for i in b:
               if i[0]==q:
                       count+=1
                       p=[q,qe,i[1]]
                       s.append(p)
           print(count)
           print(s)            
           if len(s)==0:  
               print('There no such item in the menu. Please make sure to not use \'\' with your food')
               print('\n')
           elif len(s)>count and len(s)!=0 and count!=0:  
               print('Items added successfully')
           # elif  :  
           while True:    
                try:
                    qet=int(input('Enter 2 to exit to menu or any other integer to continue ordering from this cuisine :'))
                    if qet==2:
                        count=len(s)
                        return None
                        f1.close()
                    else:
                        f1.seek(0)
                        break
                except:
                     print('Please type an integer ,continue ordering')
                     break
        except:
            print('Please enter the correct data type,continue ordering')
           

#Bill
def BILL(s):
    p=[]
    # e=0
    dish_dict = {}

    for dish in s:
        name, quantity, price = dish
        if name in dish_dict:
            dish_dict[name][0] += quantity  
        else:
            dish_dict[name] = [quantity, price]  
    for i in dish_dict:
        p.append([i,dish_dict[i][0],dish_dict[i][1]])
    print('\n')
    print(p)
    f1=open('bill.csv','w+',newline='',encoding="utf-8")
    a=csv.writer(f1)
    a.writerow(['Item name','Quantity','Price'])
    a.writerows(p)
    f1.seek(0)
    f1.close()
    total_amount=0
    print("\nBILL:")
    print(f"{'Item name':<40}{'Quantity':<15}{'Price (per unit)':<15}")
    # f1=open('bill.csv','r',encoding="utf-8")
    # b=csv.reader(f1)
    # sd=['Item name','Quantity','Price(per unit)']
    # print(sd[0],'          ',sd[1],'          ',sd[2])            
    # for i in b:
    #     print(i[0],'        ',i[1],'            ',i[2])
    #     w=int(i[2])
    #     we=int(i[1])
    #     f=(w*we)
    #     e+=f
    # print('\n')    
    # print('Total Bill(₹):',e+(e*0.05),'(Inclusive of all taxes)')
    # print('\n')
    # print('Currently only cash on Delivery is available')
    # f1.close()
    for item in p:
        name, quantity, price = item
        print(f"{name:<40}{quantity:<15}{price:<15}")
        total_amount += int(quantity) *int(price)

    # Calculate total with taxes
    tax = total_amount * 0.05
    grand_total = total_amount + tax
    print("\n")
    print(f"Subtotal: ₹{total_amount:.2f}")
    print(f"Tax (5%): ₹{tax:.2f}")
    print(f"Total Bill (₹): ₹{grand_total:.2f} (Inclusive of all taxes)\n")
    print("Currently, only Cash on Delivery is available.\n")

    while True:
        try:
            abc=input('Enter C to confirm order placement or E to cancel order :')
            if abc=='E':
                print('Your order has been canceled')
                print('Have a good day,\U0001F60A')
                return None
            elif abc=='C':
                print('Your order has been confirmed')
                print('Thank you visit again,\U0001F60A')
                return None
            else:
                print('Please type either C or E')
        except:
            print('Please make sure to type E and C and correct datatype')    

         
           
def CUSTOMERMENU():
    while True:
        a={1:'Hotel Sunshine Special',2:'South Indian',3:'Chinese Ching',4:'Vegetarian Verna',5:'Non Vegetarian Delicacies',6:'Desserts and Beverages',7:'Starters',8:'Add Ons'}
        print('='*50)
        print('               Hotel Sunshine                  ')    
        print('='*50)
        print('           Welcome to our hotel')
        print('\n')
        print('                 Cuisine ')
        print('\n')
        print('1.',a[7])
        print('2.',a[2])
        print('3.',a[3])
        print('4.',a[4])
        print('5.',a[5])
        print('6.',a[1])
        print('7.',a[6])
        print('8.',a[8])
        print('\n')
        print('9.Exit CUSTOMER MENU(Order made so far will be saved)')
        print('\n')
        print('','Hotel Mara','\n','Close to Thane Railway Station','\n','Thane-400614')
        print('='*50)
        print("Welcome to the Hotel Sunshine")
        print("Menu:")
        global s
        try:
            if len(s) > 0:
                while True:
                    try:
                        abc=input('Enter C to continue or E to pay your bill :')
                        if abc=='E':
                            # bill me chnages karna he vaise bhi end displaay joash ka kaam he
                            # yaha par voh bill ayega
                            BILL(s)
                            s=[]
                            return None
                        elif abc=='C':
                            break
                        else:
                            print('Please type either C or E')
                    except Exception as e:
                        print(e)
                        print('Please make sure to type E or C and correct datatype')
            i=eval(input('''Enter the number you want to check in the cuisine 1/2/3/4/5/6/7/8/9
OR Enter 9 to exit Customer Menu:'''))
            if i in (1,2,3,4,5,6,7,8):
                print('\n')
                MENUDISPLAY(i)
            elif i not in (1,2,3,4,5,6,7,8,9):
                print('Please select from (1,2,3,4,5,6,7,8,9)' )
            elif i==9:
                print('Exiting CUSTOMER MENU......')
                return None
        except:
            print('Please select from (1,2,3,4,5,6,7,8,9)')
         


def ADMINPANEL():
    while True:
        ab={1:'Update',2:'Delete',3:'Add Items',4:'Display'}
        print(50*'=')
        print('                ADMIN PANEL              ')
        print(50*'=')
        print('1.',ab[3])
        print('2.',ab[2])
        print('3.',ab[1])
        print('4.',ab[4])
        print('5. Exit ADMIN PANEL')
        print(50*'=')    
        try:            
            ac=int(input("Enter the number you want to check 1/2/3/4/5 from ADMIN PANEL :"))
            if ac==1:
                ADDITEMS()
            elif ac==2:
                DELETE_AND_SAVE_RECORD('Menu.csv', 'DeletedRecords.csv')
            elif ac==3:
                UPDATEITEMS()
            elif ac==4:
                DISPLAY()
            elif ac==5:
                return None
            else:
              print('Please select from 1/2/3/4/5'  )
        except:
            print('Please select from 1/2/3/4/5')


#interfacing            
while True:
    abcde={1:'Admin Panel',2:'Customer Menu',3:'Close App'}
    print(50*'=')
    print('                HOTEL SUNSHINE APP            ')
    print(50*'=')
    print('1.',abcde[1])
    print('2.',abcde[2])
    print('3.',abcde[3])
    print(50*'=')
    try:
        ad=int(input("Enter the number you want to check 1/2/3 :"))
        if ad==1:
            try:
                rt=input('Enter Admin name :')
                ty=input('Enter Admin password :')
                if rt in ('Jolebaba','Skibdi','Joash') and ty=='bankai':              
                    ADMINPANEL()
                else:
                    print('''Wrong admin name or wrong password
ACCESS DENIED                      ''')
            except:
                print('Enter string')
        elif ad==2:
           CUSTOMERMENU()
        elif ad==3:
            print('Thank you for visiting ,\U0001F60A')
            break
           
        else:
           print('Please select from 1/2/3'  )
    except:
       print('Please select from 1/2/3')