namespace ConsoleApp1
{
    public class Program
    {
        public static void Main(string[] args)
        {

#if REVIT2020
            //adsa
            File.AppendAllLines(@"C:\Users\modar\Desktop\jenkins\Jenkins\JenkinsLearn\ConsoleApp1\bin\Debug\net7.0\test.txt",new string[] { "Hello REVIT2020" });
            //ads
#else
            Console.WriteLine("Hello Issa1994");
            File.AppendAllLines(@"C:\Users\modar\Desktop\jenkins\Jenkins\JenkinsLearn\ConsoleApp1\bin\Debug\net7.0\test.txt",new string[] { "Hello Issa1994" });

#endif
            Console.ReadKey();
        }
    }
}
