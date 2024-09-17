test_list=[]
i = 1
while i < 6:
  print("Enter the list of number")
  usernumber = input("Enter username:")
  test_list.append(usernumber)
  i += 1
for num in test_list:
  if (int(num) % 2) != 0:
    print(num)
