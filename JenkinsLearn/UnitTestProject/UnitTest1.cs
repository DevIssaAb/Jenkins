namespace UnitTestProject
{
    [TestClass]
    public class UnitTest1
    {
        private const string Expected = "Hello Issa!";
        [TestMethod]
        public void TestMethod1()
        {
            using (var sw = new StringWriter())
            {
                Console.SetOut(sw);
                ConsoleApp1.Program.Main(null);

                var result = sw.ToString().Trim();
                Assert.AreEqual(Expected, result);
                //Pull Request
            }
        }
    }
}