function add()
{
    var addr1=Number(document.form1.adder1.value);
    var addr2=Number(document.form1.adder2.value);
    var result=addr1+addr2;
    // alert(addr1);
    document.form1.result.value=result;

}