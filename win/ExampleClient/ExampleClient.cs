
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace ServerTest
{
    public class Synth
    {
        public string error = null;
        public Synth()
        {
        }
        // launches RFControl.exe with Hexkey as a parameter
        // returns the port number if RFControl launch and attach to serial number were successful
        // returns -1 if unsuccessful with error containing an error message
        //
        public Int32 GetPort(string Hexkey)
        {
            try
            { 
                // get new Process object for RFcontrol
                Process p = new Process();
                // Redirect STDOUT from RFControl to us
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.RedirectStandardOutput = true;
                // RFControl.exe is in the /Program Files (x86)/SynthMachine install directory (or on 32 bit systems /Program Files/SynthMachine)
                p.StartInfo.FileName = "C:/Program Files (x86)/SynthMachine/RFControl.exe";
                // pass it Hexkey and other options (-show)
                p.StartInfo.Arguments = Hexkey;
                // Launch it and get its first line of output from STDOUT
                p.Start();            
                string output = p.StandardOutput.ReadLine();
                // Output will have port number in third parameter or an error message.
                if (!output.Contains("Can't attach"))
                {
                    //no error - split the string and and return 3rd field as Int32
                    char[] delim = { ' ' };
                    string[] fields = output.Split(delim);
                    Int32 port = Convert.ToInt32(fields[2]);
                    return port;
                }
                else
                {
                    // return with error -- error string contains error response from RFControl
                    error = output;
                    return -1;
                }
            }
            catch (Exception e)
            {
                // couldn't launch RFControl -- error string contains system exception
                error = e.Message;
                return -1;
            }  
        }
    }

    public class Client
    {
        TcpClient client = null;
        private NetworkStream stream = null;
        public Client()
        {
            
        }
        public string Connect(string serverIP, Int32 port)
        {
            try
            {
                // Create a TcpClient. 
                // The client requires a TcpServer that is connected 
                // to the same address specified by the server and port 
                // combination.
                client = new TcpClient(serverIP, port);
                stream = client.GetStream();
                return GetMessage();
            }
            catch (ArgumentNullException e)
            {
                return e.Message;
            }
            catch (SocketException e)
            {
                return e.Message;
            }
        }
        // sends message to open stream (and port), gets response and returns it.
        //
        public string SendMessage(string message)
        {
            try
            {
                // Buffer for message
                Byte[] data = new Byte[256];

                // Translate the passed message into ASCII and store it as a byte array.
                // message must be terminated with a newline
                data = System.Text.Encoding.ASCII.GetBytes(message + "\n");

                // Send the message to the connected TcpServer. 
                stream.Write(data, 0, data.Length);

                //Echo to console
                Console.WriteLine("Sent: " + message);

                // Get the Response
                return GetMessage();
            }
            catch (Exception e)
            {
                return e.Message;
            }

        }
        public string GetMessage()
        {
            try
            {
                // Buffer to store the response.  Must be big enough for largest string returned from
                // RFControl (364 bytes) or multiple reads must be issued to clear the stream from the last command
                Byte[] data = new Byte[364];

                // Read full response from stream
                Int32 bytes = stream.Read(data, 0, data.Length);
                return System.Text.Encoding.ASCII.GetString(data, 0, bytes);
            }
            catch (Exception e)
            {
                return e.Message;
            }
        }
        public void CloseConnection()
        {
            // Close the stream.
            stream.Close();
            client.Close();
        }
    }
    class Program
    {
        static void Main(string[] args)
        {
            Console.Write("Enter Hexkey: ");
            String Hexkey = Console.ReadLine();
            Synth synth = new Synth();
            Int32 port = synth.GetPort(Hexkey);
            if (port < 0)
            {
                Console.WriteLine(synth.error);
                Console.Read();
                return;
            }
           
            Client newClient = new Client();
            String e = newClient.Connect("127.0.0.1", port);
        
            if(e.Contains("Ready"))
            {
                    Console.WriteLine(e);
            } 
                else 
            {
                Console.WriteLine("Connection Error");
                Console.WriteLine(e);
                Console.Read();
                return;
            }
            Console.WriteLine("Enter 'exit' to quit");
            while (true)
            {
                Console.Write("Enter command: ");
                string message = Console.ReadLine();

                if (message == "exit")
                    break;

                Console.Write("Response: " + newClient.SendMessage(message));
                
            }
            // clean up and exit
            newClient.CloseConnection();
            Console.WriteLine("Press any key to continue...");
            Console.Read();
        }
    }


}
