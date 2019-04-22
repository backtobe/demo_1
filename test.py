myColumnName = 'id,,sname,,'
smyColumnName = myColumnName.strip().lstrip().rstrip()
amyColumnName = smyColumnName.split(",")
print(amyColumnName)
acolumn = []
for column in amyColumnName:
    if len(column) != 0:
        acolumn.append(column)
print(acolumn)
column_condition = "("
for i in range(0,len(acolumn)-1):
    column_condition += acolumn[i] + ","
if len(acolumn[-1]) != 0:
    column_condition += acolumn[-1] + ")"
print(column_condition)