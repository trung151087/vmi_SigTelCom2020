import xlrd

def readVendor(dataset,M,Hv,Price,a,b):
    file_location="in/dataset"+str(dataset)+"/Vendor.xlsx"
    wb=xlrd.open_workbook(file_location)
    sheet=wb.sheet_by_index(0)
    for i in range(1,M+1):
        Hv.append(sheet.cell_value(1,i))
        Price.append(sheet.cell_value(2,i))
        a.append(sheet.cell_value(3,i))
        b.append(sheet.cell_value(4,i))
    Av=sheet.cell_value(5,1)
    return Av

def readData(dataset):
    file_location="in/dataset"+str(dataset)+"/Data.xlsx"
    wb=xlrd.open_workbook(file_location)
    sheet=wb.sheet_by_index(0)
    return (int(sheet.cell_value(0,0)),int(sheet.cell_value(1,0)))     

def readBuyer(dataset,M,N,Hb,D,Ab):
    for j in range(0,N):
        file_location="in/dataset"+str(dataset)+"/Buyer"+str(j)+".xlsx"
        wb=xlrd.open_workbook(file_location)
        sheet=wb.sheet_by_index(0)
        for i in range(1,M):
            Hb[j][i]=sheet.cell_value(1,i)
            D[j][i]=sheet.cell_value(2,i)
        Ab[j]=sheet.cell_value(3,1)

def readSell(dataset,ngay,M,j,yban):
    file_location="in/dataset"+str(dataset)+"/SellDay"+str(ngay)+".xlsx"
    wb=xlrd.open_workbook(file_location)
    sheet=wb.sheet_by_index(0)
    for i in range(0,M):
        yban[ngay][j][i]=int(sheet.cell_value(1+j,1+i))

def readTransport(dataset,M,N,phiVanChuyen):
    for i in range (0,M):
        file_location="in/dataset"+str(dataset)+"/TransportProduct"+str(i)+".xlsx"
        wb=xlrd.open_workbook(file_location)
        sheet=wb.sheet_by_index(0)
        for j in range (0,N):
            for k in range (0,N):
                phiVanChuyen[i][j][k]=sheet.cell_value(j+1,k+1)
    
    
    