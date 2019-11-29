import random
import ReadExcel
import math

print("Su dung bo test thu:", end="")
test = int(input())
(N, M) = ReadExcel.readData(test)

Hv = []
giaSX = []
a = []
b = []
Av = ReadExcel.readVendor(test, M, Hv, giaSX, a, b)
ymin=[0 for i in range(0,M)]
ymax=[(a[i]-giaSX[i])//b[i] for i in range(0,M)]
def capNhatymax(j):
    for i in range(0,M):
        y=0
        for k in range(0,N):
            if (k!=j):
                y+=ynhap[k][i]
        temp=(a[i]-b[i]*y-giaSX[i])//b[i]    
        if (temp<=0):
            ymax[i]=0
        else:
            ymax[i]=temp

giaBan = [[0 for i in range(0, M)] for j in range (0, N)]

Hb = [[0 for i in range(0, M)] for j in range(0, N)]
Ab = [0 for j in range(0, N)]
D = [[0 for i in range(0, M)] for j in range(0, N)]
ReadExcel.readBuyer(test, M, N, Hb, D, Ab)

H = [[Hb[j][i] + Hv[i] for i in range(0, M)] for j in range(0, N)]
A = [Ab[j] + Av for j in range(0, N)]

ynhap = [[int((a[i]-giaSX[i])/(2*b[i]*N)) for i in range(0, M)] for j in range(0, N)]
def tinhLoiNhuan(j):
    Lai = 0
    phiVanChuyen = 0
    phiLuuKho = 0
    for i in range(0, M):
        phiVanChuyen += D[j][i] * ynhap[j][i]
        phiLuuKho += H[j][i] * ynhap[j][i]
        Y = 0
        for k in range(0, N): 
            Y += ynhap[k][i]
        Lai += (a[i] - b[i] * Y - giaSX[i]) * ynhap[j][i]
    return Lai - math.sqrt(2 * (A[j] + phiVanChuyen) * phiLuuKho)
loiNhuan = [(tinhLoiNhuan(j)) for j in range (0, N)]

def GA(j):
    DAN_SO = 100
    SO_THE_HE_MAX = 2000
    XAC_SUAT_LAI = 0.8
    XAC_SUAT_DOT_BIEN = 0.3

    theHe = []
    dsThichNghi = []
    
    class gtThichNghi():
        def __init__(self, giaTri, viTri):
            self.giaTri = giaTri
            self.viTri = viTri
    
    def evaluate(y): 
        Lai = 0
        phiVanChuyen = 0
        phiLuuKho = 0
        for i in range(0, M):
            phiVanChuyen += D[j][i] * y[i]
            phiLuuKho += H[j][i] * y[i]
            Y = 0
            for k in range(0, N): 
                if (k != j):
                    Y += ynhap[k][i]
            Y += y[i];
            Lai += (a[i] - b[i] * Y - giaSX[i]) * y[i]
        return Lai - math.sqrt(2 * (A[j] + phiVanChuyen) * phiLuuKho)
    
    def khoiTao(): 
        for pop in range(0,DAN_SO):
            y = []
            for i in range(0, M):
                y.append(random.randint(0, ymax[i]))
            theHe.append(y[0:])
        theHe.append(ynhap[j][0:])
        return
    
    def tienHoa():
        for i in range(DAN_SO): 
            x = random.random()
            if x < XAC_SUAT_LAI:
                lai(i)
            x = random.random()
            if x < XAC_SUAT_DOT_BIEN :
                dotBien(i)
    def lai(i):
        i2 = random.randint(0, DAN_SO - 1)
        x = random.randint(1, M - 1)
        y = theHe[i][:x] + theHe[i2][x:M]
        theHe.append(y[0:])
        
        return
    
    def dotBien(i):
        y = theHe[i][0:]
        x = random.randint(0, M - 2) 
        y[x] = random.randint(0, ymax[x])
        theHe.append(y[0:])

    def chonLoc():
        theHe.sort(key=evaluate, reverse=True)
        del theHe[DAN_SO:len(theHe)]
        return
    
    khoiTao()
    dem = 1;
    for cnt in range(SO_THE_HE_MAX):
        gt = evaluate(theHe[0])
        tienHoa()
        chonLoc()
        if (evaluate(theHe[0]) - gt <= 0.001):
            dem = dem + 1
            if dem == 10 :
                break
        else:
            gt = evaluate(theHe[0])
            dem = 1
    if (evaluate(theHe[0])-0.0001>tinhLoiNhuan(j)):
        ynhap[j] = theHe[0][0:]
        loiNhuan[j] = tinhLoiNhuan(j)

def PSO(soBien,hamMucTieu,ymin,ymax,yGbest_nhap):
    DAN_SO = 100 
    SO_THE_HE_MAX = 250
    W = 0.8
    C1 = 0.5
    C2 = 0.5
    theHe=[]
    Pbest=[0 for j in range(0,DAN_SO)]
    yPbest=[[] for j in range(0,DAN_SO)]
    yGbest=yGbest_nhap[0:]
    Gbest=hamMucTieu(yGbest)
    v=[[0 for i in range(0,soBien)] for j in range(0,DAN_SO)]
    #Khoi tao:
    for j in range(0,DAN_SO):
        y = []
        for i in range(0, soBien):
            y.append(random.randint(ymin[i],ymax[i]))
        theHe.append(y[0:])
        yPbest[j]=y
        Pbest[j]=hamMucTieu(theHe[j]) 
    #Lap:
    for gen in range(0,SO_THE_HE_MAX):
        #Cap nhat Pbest, Gbest, yGbest
        for j in range(0,DAN_SO):
            temp=hamMucTieu(theHe[j])
            if (temp>Pbest[j]):
                Pbest[j]=temp
                yPbest[j]=theHe[j][0:soBien]
                if (temp>Gbest):
                    Gbest=temp
                    yGbest=theHe[j][0:soBien]
        #Cap nhat v, y
        for j in range(0,DAN_SO):
            for i in range(0,soBien):
                v[j][i]=W*v[j][i]+random.random()*C1*(yPbest[j][i]-theHe[j][i])+random.random()*C2*(yGbest[i]-theHe[j][i])
                temp=int(theHe[j][i]+v[j][i])
                if temp>ymax[i]:
                    v[j][i]=ymax[i]-theHe[j][i]
                    theHe[j][i]=ymax[i]
                elif temp<ymin[i]:
                    v[j][i]=ymin[i]-theHe[j][i]
                    theHe[j][i]=ymin[i]
                else:
                    theHe[j][i]=temp
        #Kiem tra tinh dung
        count=0
        for j in range(0,DAN_SO):
            if Pbest[j]!=Gbest:
                count+=1
        if count==0:
            break   
    return (Gbest,yGbest)
def toiUuHoa(j):
    while (1):
        temp=tinhLoiNhuan(j)
        for i in range (0,M):
            ynhap[j][i]+=1
            if (tinhLoiNhuan(j)>temp):
                break
            ynhap[j][i]-=2
            if (tinhLoiNhuan(j)>temp):
                break
            ynhap[j][i]+=1
        else:
            loiNhuan[j]=tinhLoiNhuan(j)
            break    
def timNash():
    print("Su dung thuat toan de tim nash:")
    print("1.GA")
    print("2.PSO")
    thuatToan=int(input())
    count = 0
    for k in range(0, 1000):
        for j in range(0, N):
            capNhatymax(j)
            temp = [ynhap[j][i] for i in range(0, M)]
            if (thuatToan==1):
                GA(j)
            elif (thuatToan==2):
                def evaluate(y): 
                    Lai = 0
                    phiVanChuyen = 0
                    phiLuuKho = 0
                    for i in range(0, M):
                        phiVanChuyen += D[j][i] * y[i]
                        phiLuuKho += H[j][i] * y[i]
                        Y = 0
                        for k in range(0, N): 
                            if (k != j):
                                Y += ynhap[k][i]
                        Y += y[i];
                        Lai += (a[i] - b[i] * Y - giaSX[i]) * y[i]
                    return Lai - math.sqrt(2 * (A[j] + phiVanChuyen) * phiLuuKho)
                (loiNhuan[j],ynhap[j])=PSO(M,evaluate,ymin,ymax,ynhap[j])
            toiUuHoa(j)
            print("ynhap=", ynhap)
            print("    Loi Nhuan=", loiNhuan)
            if (temp == ynhap[j]):
                count += 1
                
                if (count == N):
                    print("Can bang nash:", ynhap)
                
                    return
            else:
                
                count = 0

            
def checkNash():
    for j in range(0, N):
        for i in range(0, M):
            temp1 = tinhLoiNhuan(j)
            ynhap[j][i] += 1
            temp2 = tinhLoiNhuan(j)
            ynhap[j][i] -= 2
            temp3 = tinhLoiNhuan(j)
            ynhap[j][i] += 1
            if (temp1 < temp2):
                print("Day chua phai Nash")
                print("Co the tang y[", j, "][", i, "] them 1 don vi")
                return 0
            if (temp1 < temp3):
                print("Day chua phai Nash")
                print("Co the giam y[", j, "][", i, "] di 1 don vi")
                return 0
    return 1        


#------------------------MAIN------------------------
timNash()
if (checkNash()==1):
    print("Dieu kien can bang Nash duoc thoa man")
print("Loi nhuan:", loiNhuan)
while (1):
    print()
    print("Thay doi retailer thu:", end="")
    jnew = int(input())
    print("Thay doi mat hang thu:", end="")
    inew = int(input())
    print("So luong hang nhap moi:", end="")
    ynhapnew = int(input())
    for j in range (0, N):
        loiNhuan[j] = tinhLoiNhuan(j)
    print("Can bang nash:", ynhap)
    print("Loi nhuan:", loiNhuan)
    ynhap[jnew][inew] = ynhapnew
    for j in range (0, N):
        loiNhuan[j] = tinhLoiNhuan(j)
    print("So hang nhap:", ynhap)
    print("Loi nhuan:", loiNhuan)
    if (checkNash()==1):
        print("Dieu kien can bang Nash duoc thoa man")
input()
        
