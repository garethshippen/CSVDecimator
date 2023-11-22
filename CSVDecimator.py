from csv import DictReader
from csv import DictWriter

class CSVDecimator():
    def __init__(self, filename, divisions = 10, header = "Branching Logic (Show field only if...)"):
        self.filename = filename
        self.divisions = divisions
        self.header = header
        self.rows = []
        self.copy = []
        with open(filename, 'r') as file:
            data = DictReader(file)
            self.fieldnames = data.fieldnames
            for row in data:
                self.rows.append(row)
        with open(filename, 'r') as file:
            dupe = DictReader(file)
            for row in dupe:
                self.copy.append(row)
        CSVDecimator.clear_column(self.copy, self.header)

    def clear_column(data, header):
        for row in data:
            row[header] = ""

    def set_divisions(self, divisions):
        self.divisions = divisions
        
    def set_header(self, header):
        self.header = header
        
    def decimate(self):
        length = len(self.rows)
        share = (int)(length/self.divisions)
        self.slices = []
        for i in range(self.divisions + 1):
            self.slices.append([self.rows[i * share:(i+1)*share], self.copy[i * share:(i+1)*share]])
            
    def generate(self):
        for i in range(len(self.slices)):
            outfile = self.filename[:-4] + str(i) + self.filename[-4:]
            corpus = []
            for j in range(len(self.slices)):
                if i != j:
                    corpus += self.slices[j][1]
                else:
                    corpus += self.slices[j][0]
            with open(outfile, 'w', newline = "") as out:
                writer = DictWriter(out, self.fieldnames)
                writer.writeheader()
                for row in corpus:
                    writer.writerow(row)
                    
                    
if __name__ == "__main__":
    decimator = CSVDecimator("base.csv")
    decimator.decimate()
    decimator.generate()