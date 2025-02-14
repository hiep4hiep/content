## Create Application & Token in Aruba Central
Follow the instruction here https://www.arubanetworks.com/techdocs/central/2.5.4/content/pdfs/central/api-reference-guide.pdf

To create an application, complete the following steps:
1. In the Account Home page, under Global Settings, click API Gateway.
The API Gateway page is displayed.
2. Click the My Apps & Tokens tab.
3. Click + Add Apps & Tokens.
4. In the New Token pop-up window, do the following:
a. Enter the application name. In non-admin user profile, the Application Name field contains the
logged-in user name and is non-editable.
b. In the Redirect URI field, enter the redirect URL.
c. From the Application drop-down list, select the application.
d. Click Generate. A new application is created and added to the My Apps & Tokens table.

5. The Token List table displays the following:
- Token ID—Token ID of the application.
- User Name—Name of the user to whom this token is associated to. An application can be associated to multiple users.
- Application—Name of the application to which this token is associated to. For example, Network Operations.
- Generated At—Date on which the token was generated.
- Revoke Token—Click Revoke Token and click Yes to revoke the token associated to a particular user. For example, if two users are associated to an application and if you want to remove access to a particular user, revoke the token associated to that user.
- Download Token—Click Download Token to download the token

## Configure the integration
1. Use the Token downloaded from the step 5 above as input in the API Token integration parameter

