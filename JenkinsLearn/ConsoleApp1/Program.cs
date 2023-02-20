namespace ConsoleApp1
{
  
    public class Program
    {
      
      
        public static void Main(string[] args)
        {
          
#if REVIT2020
            Console.WriteLine("Hello REVIT2020");
            File.AppendAllLines(@"C:\Users\modar\Desktop\jenkins\Jenkins\JenkinsLearn\ConsoleApp1\bin\Debug\net7.0\test.txt",new string[] { "Hello REVIT2020" });
#else
            //dasd
            Console.WriteLine("Hello Issa1994");
          //cxzcz
            File.AppendAllLines(@"C:\Users\modar\Desktop\jenkins\Jenkins\JenkinsLearn\ConsoleApp1\bin\Debug\net7.0\test.txt",new string[] { "Hello Issa1994" });

#endif
//dasds
            Console.ReadKey();
          
          //cxzc
//czxc
        }
    }
}
