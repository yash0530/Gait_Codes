import java.io.*;
import java.net.*;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;

public class QuoteClient {
    public static void main(String[] args) throws IOException, UnknownHostException, SecurityException
    {
    	DatagramPacket mDatagramPacket =null;
    	DatagramSocket mDatagramSocket = null;

		InetAddress client_adress = null;
        try {
            client_adress = InetAddress.getByName("172.20.10.5");
        } catch (UnknownHostException e) {
            return ;
        }
        try {
            mDatagramSocket = new DatagramSocket(5555, client_adress);
            mDatagramSocket.setReuseAddress(true);
        } catch (SocketException e) {
            mDatagramSocket = null;
            return ;
        }

        byte[] buf = new byte[256];

        try {
            mDatagramPacket = new DatagramPacket(buf, buf.length, client_adress, 5555);
        } catch (Exception e) {
        	mDatagramSocket.close();
        	mDatagramSocket = null;
        	return;
        }

        BufferedWriter mBufferwriter = new BufferedWriter(new FileWriter("test.csv"));
        StringBuilder prevText = new StringBuilder();
        while(true)
        {
            try {
                mDatagramSocket.receive(mDatagramPacket);
                String text = new String(mDatagramPacket.getData(),0, mDatagramPacket.getLength());

                if (!prevText.toString().equals(text)) {
                    System.out.println(text);
                    mBufferwriter.write(text + "\r\n");
                    mBufferwriter.flush();
                }

                int l = prevText.length();
                prevText.replace(0, l, text);
            } catch (Exception e) {
                e.printStackTrace();
                break;
            }
        }
    }
}
