import mysqlx
from datetime import date, timedelta

def insert_vehicle(connection):

    try:
        schema = connection.get_schema("rental")
        table = schema.get_table("vehicle")

        v_name = input("Enter vehicle name: ")
        reg_no = input("Enter registration number: ")
        v_rent = int(input("Enter rent per day: "))
        fuel_type = input("Enter fuel type: ")
        category = input("Enter category (5/7/13): ")

        table.insert(["v_name","reg_no","v_rent","fuel_type","category","status"]).values(v_name,reg_no,v_rent,fuel_type,category,"available").execute()
        print("Vehicle Added Successfully!")

    except Exception as e:
        print(type(e))
        print(repr(e))

def select_vehicle(connection):
    try:
        qry = "select v_id,v_name,reg_no,v_rent,fuel_type,category,status from vehicle"
        result = connection.sql(qry).execute()
        print("_"*120)
        print("ID \t NAME \t REG NO \t RENT \t FUEL \t CATEGORY \t STATUS")
        print("_"*120)

        for row in result.fetch_all():
            print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                    row["v_id"],row["v_name"],row["reg_no"],row["v_rent"],row["fuel_type"], row["category"],row["status"]
                )
            )
    except Exception as e:
        print(type(e))
        print(repr(e))

def change_vehicle_status(connection):
    try:
        schema = connection.get_schema("rental")
        table = schema.get_table("vehicle")

        v_id = int(input("Enter Vehicle ID: "))

        print("1. Available")
        print("2. Rented")
        print("3. Maintenance")

        ch = input("Enter choice: ")

        if ch == "1":
            status = "available"
        elif ch == "2":
            status = "rented"
        elif ch == "3":
            status = "maintenance"
        else:
            print("Invalid Choice")
            return

        table.update().set("status", status).where("v_id=:id").bind("id", v_id).execute()
        print("Status Updated Successfully!")

    except Exception as e:
        print(type(e))
        print(repr(e))

def delete_vehicle(connection):
    try:
        schema = connection.get_schema("rental")
        table = schema.get_table("vehicle")

        v_id = int(input("Enter Vehicle ID to Delete: "))
        result = table.select("v_id").where("v_id=:id").bind("id", v_id).execute()
        row = result.fetch_one()

        if row:
            table.delete().where("v_id=:id").bind("id", v_id).execute()
            print("Vehicle Deleted Successfully!")
        else:
            print("Vehicle Not Found")

    except Exception as e:
        print(type(e))
        print(repr(e))

def insert_customer(connection):
    try:
        schema = connection.get_schema("rental")
        table = schema.get_table("customer")

        c_name = input("Enter Customer Name: ")
        c_contact_no = input("Enter Contact Number: ")
        c_address = input("Enter Address: ")
        table.insert(["c_name", "c_contact_no","c_address"]).values(c_name,c_contact_no,c_address).execute()
        print("Customer Added Successfully!")

    except Exception as e:
        print(type(e))
        print(repr(e))

def select_customer(connection):
    try:
        qry = "select c_id,c_name,c_contact_no,c_address from customer"
        result = connection.sql(qry).execute()

        print("_"*100)
        print("ID \t NAME \t CONTACT \t ADDRESS")
        print("_"*100)

        for row in result.fetch_all():
            print("{}\t{}\t{}\t{}".format(row["c_id"],row["c_name"],row["c_contact_no"],row["c_address"]))

    except Exception as e:
        print(type(e))
        print(repr(e))

def delete_customer(connection):
    try:
        schema = connection.get_schema("rental")
        table = schema.get_table("customer")

        c_id = int(input("Enter Customer ID to Delete: "))
        result = table.select("c_id").where("c_id=:id").bind("id", c_id).execute()
        row = result.fetch_one()

        if row:
            table.delete().where("c_id=:id").bind("id", c_id).execute()
            print("Customer Deleted Successfully!")
        else:
            print("Customer Not Found")

    except Exception as e:
        print(type(e))
        print(repr(e))

def rent_vehicle(connection):
    try:
        schema = connection.get_schema("rental")

        qry = "select v_id, v_name, reg_no,v_rent from vehicle where status='available'"
        result = connection.sql(qry).execute()
        print("\n AVAILABLE VEHICLES")
        print("_"*100)

        for row in result.fetch_all():
            print("{}\t{}\t{}\t{}".format(row["v_id"],row["v_name"],row["reg_no"],row["v_rent"]))

        print("\n CUSTOMERS")
        result = connection.sql("select c_id,c_name from customer").execute()

        for row in result.fetch_all():
            print("{}\t{}".format(row["c_id"],row["c_name"]))

        c_id = int(input("\nEnter Customer ID: "))
        qry = f"SELECT r_id FROM rent WHERE c_id = {c_id} AND rent_status = 'active'"
        result = connection.sql(qry).execute()
        row = result.fetch_one()

        if row is not None:
            print("This customer already has an active rental.")
            print("A customer can rent only one vehicle at a time.")
            return
                
        v_id = int(input("Enter Vehicle ID: "))
        rent_days = int(input("Enter Rent Days: "))

        vehicle_table = schema.get_table("vehicle")

        result = vehicle_table.select("v_name","v_rent","status").where("v_id=:id").bind("id",v_id).execute()
        vehicle = result.fetch_one()

        if vehicle is None:
            print("Vehicle Not Found")
            return

        if vehicle[2] != "available":
            print("Vehicle is not available for rent")
            return

        v_name = vehicle[0]
        rent_per_day = vehicle[1]

        total_amount = rent_per_day * rent_days

        return_date = date.today() + timedelta(days=rent_days)

        print("\n===== RENT SUMMARY =====")
        print("Vehicle :", v_name)
        print("Rent Days :", rent_days)
        print("Return Date :", return_date)
        print("Total Amount :", total_amount)

        confirm = input("\nConfirm Rent (Y/N): ")
        if confirm.upper() != "Y":
            print("Rent Cancelled")

            return
        
        rent_table = schema.get_table("rent")
        rent_table.insert(["v_id","c_id","rent_days","total_amount","return_date","rent_status"]).values(v_id,c_id,rent_days,total_amount,str(return_date),"active").execute()

        vehicle_table.update().set("status", "rented").where("v_id=:id").bind("id", v_id).execute()

        print("\n Vehicle Rented Successfully!")
        print("Happy Journey 😃")

    except Exception as e:
        print(type(e))
        print(repr(e))

def return_vehicle(connection):
    try:
        qry = "select r_id,v_id,c_id,rent_status from rent where rent_status='active'"
        result = connection.sql(qry).execute()

        rows = result.fetch_all()

        if len(rows) == 0:
            print("\nNo vehicles to return.")
            return

        print("\n---- RENT RECORDS ----")
        print("Rent ID\tVehicle ID\tCustomer ID\tStatus")
        print("-"*50)

        for row in rows:
            print("{}\t{}\t\t{}\t\t{}".format(
                row["r_id"],
                row["v_id"],
                row["c_id"],
                row["rent_status"]
            ))
        
        while True:
            rent_id = int(input("Enter Rent ID: "))

            qry = f"select v_id from rent where r_id={rent_id} and rent_status='active'"
            result = connection.sql(qry).execute()
            row = result.fetch_one()

            if row is not None:
                break

            print("Invalid Rent ID. Please try again.")

        v_id = row[0]
        schema = connection.get_schema("rental")
        rent_table = schema.get_table("rent")

        rent_table.update().set("rent_status", "returned").where("r_id=:id").bind("id", rent_id).execute()
        vehicle_table = schema.get_table("vehicle")
        vehicle_table.update().set("status", "available").where("v_id=:id").bind("id", v_id).execute()

        print("Vehicle Returned Successfully!")
    except Exception as e:
        print(type(e))
        print(repr(e))

def rental_history(connection):
    try:
        qry = """select r.r_id,c.c_name,v.v_name,v.reg_no,r.rent_days,r.return_date,r.total_amount,r.rent_status
        from rent r join customer c on r.c_id = c.c_id join vehicle v on r.v_id = v.v_id"""

        result = connection.sql(qry).execute()

        print("_"*120)
        print("RID\tCUSTOMER\tVEHICLE\tREGNO\tDAYS\tRETURN DATE\tAMOUNT\tSTATUS")
        print("_"*120)

        for row in result.fetch_all():
            print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}"
                .format(row["r_id"],row["c_name"],row["v_name"],row["reg_no"],
                row["rent_days"],row["return_date"],
                row["total_amount"],row["rent_status"]))

    except Exception as e:
        print(type(e))
        print(repr(e))

try:
    conn = mysqlx.get_session({

        "host":"localhost",
        "port":33060,
        "user":"root",
        "password":"Amolbav@123",
        "compression":"disabled"
    })

    conn.sql("USE rental").execute()

except Exception as e:
    print(type(e))
    print(repr(e))
    exit()

print("\n===== VEHICLE RENTAL SYSTEM =====")
while True:

    print("\n1. Vehicle")
    print("2. Customer")
    print("3. Rent Vehicle")
    print("4. Return Vehicle")
    print("5. Rental History")
    print("6. Exit")

    ch = int(input("Enter Choice: "))

    if ch == 1:
        while True:
            print("\n===== VEHICLE MENU =====")

            print("1. Add Vehicle")
            print("2. View Vehicles")
            print("3. Change Vehicle Status")
            print("4. Delete Vehicle")
            print("5. Back")

            v = int(input("Enter Choice: "))

            if v == 1:
                insert_vehicle(conn)
            elif v == 2:
                select_vehicle(conn)
            elif v == 3:
                change_vehicle_status(conn)
            elif v == 4:
                delete_vehicle(conn)
            elif v == 5:
                break

    elif ch == 2:
        while True:
            print("\n===== CUSTOMER MENU =====")

            print("1. Add Customer")
            print("2. View Customers")
            print("3. Delete Customer")
            print("4. Back")

            c = int(input("Enter Choice: "))

            if c == 1:
                insert_customer(conn)
            elif c == 2:
                select_customer(conn)
            elif c == 3:
                delete_customer(conn)
            elif c == 4:
                break

    elif ch == 3:
        rent_vehicle(conn)
    elif ch == 4:
        return_vehicle(conn)
    elif ch == 5:
        rental_history(conn)
    elif ch == 6:
        conn.close()
        print("Thank You For Using Vehicle Rental System")
        break
    else:
        print("Invalid Choice")