/**
 * Created by rainer on 1/18/14.
 */



function replaceComillaDoble(str)
{
   var spli = str.split('&quot;')
   var string = ""
   for(var i=0; i < spli.length;i++)
   {
       if(i != 0)
         string+='"'+spli[i]
       else
         string+=spli[i]
   }

   return string
}

