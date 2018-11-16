import mosspy
import sys

SUBMISSIONS = "submissions/*/*.py"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python moss.py [Moss ID]")
        sys.exit(1)
    userid = sys.argv[1]
    print("Moss ID:", userid, "Submissions:", SUBMISSIONS)
    print("Moss is running. Please be patient. It may take around 5 mintues to generate the result.")
    sys.exit(0)
    m = mosspy.Moss(userid, "python")
    m.addFilesByWildcard(SUBMISSIONS)

    url = m.send() # Submission Report URL

    print("Report Url: " + url)
    print(url)
    # Save report file
    m.saveWebPage(url, "./mossreport.html")

    # Download whole report locally including code diff links
    mosspy.download_report(url, "report/", connections=8)
