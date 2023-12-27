from modified_login_page import *

load_dotenv()  

# Access the MySQL password using the environment variable
mysql_password = os.getenv("MYSQL_PASSWORD")

mydb = MySQLdb.connect(host="localhost", user="root", passwd=mysql_password, database="banking_management_system")
mycursor = mydb.cursor()

# Main application window
root = Tk()
root.title("Welcome to the Banking System!!!")

obj = Login(root, mycursor, mydb)

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))  # Full screen

# Create a canvas to display the background
canvas = Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack()

left_image = Image.open("images/blue_sky.jpeg")
right_image = Image.open("images/green_grass.jpeg")

canvas_width = canvas.winfo_reqwidth()
canvas_height = canvas.winfo_reqheight()

# Resize the images to match the canvas size
left_image_cropped = left_image.crop((0, 0, canvas_width // 2, canvas_height))
right_image_cropped = right_image.crop((canvas_width // 2, 0, canvas_width, canvas_height))

# Convert the cropped images to PhotoImage
left_background_image = ImageTk.PhotoImage(left_image_cropped)
right_background_image = ImageTk.PhotoImage(right_image_cropped)

# Create left background image
canvas.create_image(0, 0, anchor=NW, image=left_background_image)
canvas.image = left_background_image  # Keep a reference to prevent garbage collection

# Create right background image
canvas.create_image(canvas.winfo_reqwidth() // 2, 0, anchor=NW, image=right_background_image)
canvas.image = right_background_image

# Add main heading
main_heading = Label(root, text="Welcome to the Banking System!!!", font=("Helvetica", 24, "bold"))
main_heading.place(relx=0.5, rely=0.2, anchor="center")

# Add subheading
subheading = Label(root, text="Who are you?", font=("Helvetica", 18))
subheading.place(relx=0.5, rely=0.3, anchor="center")

# Add buttons
customer_button = Button(root, text="Customer", font=("Helvetica", 16), command=obj.register_or_login)
employee_button = Button(root, text="Employee", font=("Helvetica", 16), command=obj.employee_login)

customer_button.place(relx=0.3, rely=0.5, anchor="center")
employee_button.place(relx=0.7, rely=0.5, anchor="center")
        
root.mainloop()