from csv import writer
from csv import reader

def add_column_in_csv(input_file, output_file, transform_row):
	with open(input_file, 'r') as read_obj, \
            open(output_file, 'w', newline='') as write_obj:
        csv_reader = reader(read_obj)
        csv_writer = writer(write_obj)
         for row in csv_reader:
            # Pass the list / row in the transform function to add column text for this row
            transform_row(row, csv_reader.line_num)
            # Write the updated row / list to the output file
            csv_writer.writerow(row)

def merge_csvs(prng):
	add_column_in_csv("compression_ratio_cluster_data_"+str(prng)+".csv", "/cluster_data/sp800_collected_cluster_data_" + str(prng) + ".csv", lambda row, line_num: row.append(row[0]))