import java.io.File;
import java.io.IOException;
import java.util.Scanner;
import java.util.regex.*;
public class spellcheck
{
	public void words(String text)
	{
		try
		{
			String trainingText = readFile("big.txt");
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}

		Pattern pattern = Pattern.compile("[a-z']+|[a-z]");
		Matcher matcher = pattern.matcher(trainingText);
	}
	private String readFile(String pathname) throws IOException
	{

		File file = new File(pathname);
		StringBuilder fileContents = new StringBuilder((int)file.length());
		Scanner scanner = new Scanner(file);
		String lineSeperator = System.getProperty("line.seperator");

		try
		{
			while(scanner.hasNextLine())
			{
				fileContents.append(scanner.nextLine()+lineSeperator);
			}
			return fileContents.toString();
		}
		finally
		{
			scanner.close();
		}
	}
}