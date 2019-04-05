<h3> TL1 Fiberhome</h3>
<h4> A script to configure multiple ONUs using csv data<h4>

<h5> Data needed </h5>
<p> 
csv file1: serial,pppoe username, mac address.
<br>
csv file2: slot, pon, serial, model
</p>

<h5> Explanation <h5>
<p>The csv file 1 you will get from your database of clientes. 
This infomations usually are saved on this database.</p>
<p>The csv file 2 you will get from the UNM2000, this is what you will do: After reset the OLT
you will set all PONs to NO_AUTH, when you do that, all ONUs will authenticate and now you have
all the serials, slot, and pon on UNM2000. You just have to export all (right click and then export).
After that you can return the pon to PHYS_ID_AUTH
<p>

<p> For define the vlans. Please modify the function: tl1functions.calc_vlanid or 
you can create a dictionary and make the fork that i will check. </p>
<h5> Requirements </h5>
<p> 
Pandas
<br>
Internet Connection
<br>
Python 3
</p>
