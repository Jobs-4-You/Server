# import scheduler.client
from j4u_api.qualtrics import qual_client

# x = qual_client.create_contact(email="ather@test.com")
a = qual_client.list_surveys()
x = a[0]["id"]
print(x)

y = qual_client.list_distributions(x)

print(y)
