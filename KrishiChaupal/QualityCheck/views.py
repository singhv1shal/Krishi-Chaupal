from django.shortcuts import render
from .forms import UploadImage
from django.http import HttpResponseRedirect
import cv2
import numpy as np
import time
# Create your views here.
infmsg="Your crop quality Result"
precmsg="Precautions here"

def ImageProcessing(img_name):
    print(img_name)
    filename="QualityCheck/media/Leaves/"+img_name.name
    print(filename)
    # time.sleep(3)
    img=cv2.imread(filename)
    img = cv2.resize(img ,((int)(img.shape[1]/5),(int)(img.shape[0]/5)))
    original = img.copy()
    neworiginal = img.copy()

    p = 0
    for i in range(img.shape[0]):
    	for j in range(img.shape[1]):
    		B = img[i][j][0]
    		G = img[i][j][1]
    		R = img[i][j][2]
    		if (B > 110 and G > 110 and R > 110):
    			p += 1

    #finding the % of pixels in shade of white
    totalpixels = img.shape[0]*img.shape[1]
    per_white = 100 * p/totalpixels
    '''
    print 'percantage of white: ' + str(per_white) + '\n'
    print 'total: ' + str(totalpixels) + '\n'
    print 'white: ' + str(p) + '\n'
    '''

    #excluding all the pixels with colour close to white if they are more than 10% in the image
    if per_white > 10:
    	img[i][j] = [200,200,200]
    	#cv2.imshow('color change', img)


    #Guassian blur
    blur1 = cv2.GaussianBlur(img,(3,3),1)


    #mean-shift algo
    newimg = np.zeros((img.shape[0], img.shape[1],3),np.uint8)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER , 10 ,1.0)

    img = cv2.pyrMeanShiftFiltering(blur1, 20, 30, newimg, 0, criteria)
    #cv2.imshow('means shift image',img)


    #Guassian blur
    blur = cv2.GaussianBlur(img,(11,11),1)

    #Canny-edge detection
    canny = cv2.Canny(blur, 160, 290)

    canny = cv2.cvtColor(canny,cv2.COLOR_GRAY2BGR)
    #creating border around image to close any open curve cut by the image border
    #bordered = cv2.copyMakeBorder(canny,10,10,10,10, cv2.BORDER_CONSTANT, (255,255,255))		#function not working(not making white coloured border)
    #bordered = cv2.rectangle(canny,(-2,-2),(275,183),(255,255,255),3)
    #cv2.imshow('Canny on meanshift bordered image',bordered)


    #contour to find leafs
    bordered = cv2.cvtColor(canny,cv2.COLOR_BGR2GRAY)
    contours,hierarchy = cv2.findContours(bordered, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    maxC = 0
    maxid=0
    for x in range(len(contours)):													#if take max or one less than max then will not work in
    	if len(contours[x]) > maxC:													# pictures with zoomed leaf images
    		maxC = len(contours[x])
    		maxid = x

    perimeter = cv2.arcLength(contours[maxid],True)
    #print perimeter
    Tarea = cv2.contourArea(contours[maxid])
    cv2.drawContours(neworiginal,contours[maxid],-1,(0,0,255))
    #cv2.imshow('Contour',neworiginal)
    #cv2.imwrite('Contour complete leaf.jpg',neworiginal)



    #Creating rectangular roi around contour
    height, width, _ = canny.shape
    min_x, min_y = width, height
    max_x = max_y = 0
    frame = canny.copy()

    # computes the bounding box for the contour, and draws it on the frame,
    for contour, hier in zip(contours, hierarchy):
    	(x,y,w,h) = cv2.boundingRect(contours[maxid])
    	min_x, max_x = min(x, min_x), max(x+w, max_x)
    	min_y, max_y = min(y, min_y), max(y+h, max_y)
    	if w > 80 and h > 80:
    		#cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 0), 2)   #we do not draw the rectangle as it interferes with contour later on
    		roi = img[y:y+h , x:x+w]
    		originalroi = original[y:y+h , x:x+w]

    if (max_x - min_x > 0 and max_y - min_y > 0):
    	roi = img[min_y:max_y , min_x:max_x]
    	originalroi = original[min_y:max_y , min_x:max_x]
    	#cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)   #we do not draw the rectangle as it interferes with contour

    #cv2.imshow('ROI', frame)
    #cv2.imshow('rectangle ROI', roi)
    img = roi


    #Changing colour-space
    #imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imghls = cv2.cvtColor(roi, cv2.COLOR_BGR2HLS)
    #cv2.imshow('HLS', imghls)
    imghls[np.where((imghls==[30,200,2]).all(axis=2))] = [0,200,0]
    #cv2.imshow('new HLS', imghls)

    #Only hue channel
    huehls = imghls[:,:,0]
    #cv2.imshow('img_hue hls',huehls)
    #ret, huehls = cv2.threshold(huehls,2,255,cv2.THRESH_BINARY)

    huehls[np.where(huehls==[0])] = [35]
    #cv2.imshow('img_hue with my mask',huehls)


    #Thresholding on hue image
    ret, thresh = cv2.threshold(huehls,28,255,cv2.THRESH_BINARY_INV)
    #cv2.imshow('thresh', thresh)


    #Masking thresholded image from original image
    mask = cv2.bitwise_and(originalroi,originalroi,mask = thresh)
    #cv2.imshow('masked out img',mask)


    #Finding contours for all infected regions
    contours,heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    Infarea = 0
    for x in range(len(contours)):
    	cv2.drawContours(originalroi,contours[x],-1,(0,0,255))
    	#cv2_imshow('Contour masked',originalroi)

    	#Calculating area of infected region
    	Infarea += cv2.contourArea(contours[x])

    if Infarea > Tarea:
    	Tarea = img.shape[0]*img.shape[1]

    print(perimeter)
    print(Infarea)
    print(Tarea)
    per=(Infarea/Tarea)*100
    context={}
    if per>25:
        context.update({'infected':'Yes','Infarea':Infarea,'Tarea':Tarea,'perimeter':perimeter})
    else:
        context.update({'infected':"No",'Infarea':'12.3','Tarea':Tarea,'perimeter':perimeter})
    return context

def message(s,con):
    ans={}
    infmsg="Your leaf infected area is "+str(con['Infarea'])+" out of total area "+str(con['Tarea'])+" "
    if s in ['Rice','rice']:
        infmsg+="Your crop may be affected by the following: '\n' 1. Thrips '\n' 2. Green leafhopper '\n' 3. Brown plant hopper"
        precmsg="In Thrips you observe that both nymphs and adults lacerate the tender leaves and suck the plant sap, causing yellow or silvery streaks on the leaves of young seedlings. You will be needed to spray endosu fan 35 EC 80 ml or monocrotophos 36 WSC 40 ml/800 m2 nursery. In Green leafhopper you may observe that both nymphs and adults desap the leaves and cause “hopper burn” due to heavy infestation.You may also observe yellowing of leaves from tip downwards. For prevention use resistant varieties like IR 20, IR 50, CR 1009, Co 46, PTB 2, PTB 18, IET 7301, IET 7302, IET 7303 and Vani, Vikra marka, Lalit, Nidhi."
    if s in ['Maize','maize']:
        infmsg+="Your crop may be affected by the following: 1. Maize shootfly 2. Stem borer 3. Pink stem borer.  In maize shootfly the maggot feeds on the young growing shoots resulting in “dead hearts."
        precmsg="You can grow resistant cultivars like DMR 5, NCD, VC 80 . In stem borer the crop infests a month after sowing and upto emergence of cobs.The typical damage symptom is Central shoot withering leading to “dead heart”. You can grow resistant cultivars like Him 129, Ganga 4,5,7 and 9, Ganga safed 2, Deccan 101 and 103, Him 123, Ageti, C 1, 3 and 7, Kanchan, Kundan. In pink stem borer Pink larva enters into the stem causing dead heart symptom similar to that of stem borer. You can grow resistant cultivars like Deccan 101 and 103."
    if s in ['Wheat','wheat']:
        infmsg+="Your crop may be affected by the following: 1. Wheat Aphid 2. Climbing cutworm/armyworm 3. Ghujhia Weevil In wheat Aphid Like other aphids, the nymphs and adults suck the sap from plants, particularly from their ears. They appear on young leaves or ears in large numbers during the cold and cloudy weather"
        precmsg="As prevention you can spray 375 ml of dimethoate 30 EC or oxydemeton methyl 25 EC or monocrotophos 36SL in 500 L of water per ha. In climbing cutworm the freshly emerged larvae spin threads from which they suspend themselves in the air and then with the help of air currents reach from one plant to another.In the case of a severe attack, whole leaves, including the mid-rib, are consumed and the field looks as if grazed by cattle. The pest can be suppressed by collecting and destroying the caterpillars. In ghujhia weevil only adults feed on leaves and tender shoots of the host plants. They cut the germinating seedlings at the ground level. As a prevention use dust carbaryl or malathion 5 D @ 25 kg per ha."
    if s in ['Pulses','pulses']:
        infmsg+="Your crop may be affected by the following: 1. Bean aphid 2. Thrips 3. Whitefly In bean aphid both nymphs and adults cause the damage by sucking the plant sap. Infested pods become deshaped, withered and malformed. Severe infestation may result in complete drying of affected pods.."
        precmsg="You can grow resistant cowpea cultivars like P 1473, P 1476, MS 9369, Bendel Lobia 1. In thrips the leaves are mottled with characteristic silvering due to the attack of insect especially under dry spell on lab lab, black gram, green gram, cow pea. Later leaves dry and shed. You can spray Malathion 50 EC 1.0 L or Carbaryl 50 WP 1.0 kg in 700 L water. In whitefly the damage is caused by both nymphs and adults, which are found in large numbers. They suck plant sap and lower its vitality. You can grow black gram resistant varieties like ML 337, ML 5, MH 85-61, ML 325."
    if s in ['Cotton','cotton']:
        infmsg+="Your crop may be affected by the following: 1. Leafhopper 2. Cotton aphid 3. Thrips In leafhopper both nymphs and adults suck the sap from the under surface of leaves, tender leaves turn yellow, leaf margins curl downwards and reddening sets in."
        precmsg="Prevention suggested as early sowing and close spacing of cotton reduces pest infestation particularly if the rainfall is heavy . The cotton aphid is a potential pest on cotton infesting tender shoots and under surface of the leaves. They  occur in large numbers, suck the sap and cause stunted growth, gradual drying resulting in death of the plants. As prevention you can monitor the nymphs and adults of early season sucking pests from the 14th day after sowing. In thrips both nymph and adult lacerate the tissue and suck the sap from the upper and lower surface of leaves and in cases of severe infestation they curl up and become crumbled.As prevention you can monitor the nymphs and adults from the 14th day after sowing."
    if s in ['Sugarcane','sugarcane']:
        infmsg+="Your crop may be affected by the following: 1. Early shoot borer 2. Internode borer 3. Top borer In Early shoot borer you observe dead heart in 1-3 month old crop, which can be easily pulled out, rotten portion of the straw coloured deadheart emits an offensive odour."
        precmsg="As prevention you can apply management practice if population excess ETL of 15% dead heart. In Internode borer Internodes constricted and shortened, with a number of boreholes and fresh excreta in the nodal region. Affected tissues become reddened. As a prevention avoid use of excessive nitrogen fertilizers also release egg parasitoid. In Top borer dead heart in grown up canes is observed, which cannot be easily pulled; dead heart is reddish brown in colour. You can grow resistant varieties: Co 724, CoJ 67, Co 1158, Co 1111 also Collect and destroy the egg masses to prevent the crop."
    if s in ['Tomato','tomato']:
        infmsg+="Your crop may be affected by the following: 1. Fruit borer 2. Serpentine leaf miner3. Leaf eating caterpillar In fruit borer both nymphs and adults suck the sap from the under surface of leaves, tender leaves turn yellow, leaf margins curl downwards and reddening sets in. Single caterpillar can destroy 2-8 fruits."
        precmsg="To prevent the crop collect and destroy the infested fruits and grown up larvae. Also you can row less susceptible genotypes Rupali, Roma, Pusa red plum. In serpentine leaf miner Maggots mines into leaves and cause serpentine mines drying and drooping of leaves. For prevention of crops collect and destroy mined leaves also spray NSKE 5% . In leaf eating caterpillar both nymph and adult lacerate the tissue and suck the sap from the upper and lower surface of leaves and in cases of severe infestation they curl up and become crumbled. As prevention you can monitor the nymphs and adults from the 14th day after sowing."
    if s in ['Onion','onion']:
        infmsg+="Your crop may be affected by the following: 1. Onion thrips 2. Onion maggot 3. Earwig In Onion thrips adults as well as by nymphs lacerate the leaf tissue and feed on the plant juice. The insects are just visible to the unaided eye and are seen moving briskly on the flowers and leaves of onion and garlic plants."
        precmsg="As a prevention grow resistant varieties viz., White Persian, Grano, Sweet Spanish and Crystal Wax. In Onion maggot the maggots bore into the bulbs, causing the plants to become flabby and yellowish. It causes withering in the field and rotting in storage. As a prevention grow Allium fistulosum as it is more tolerant than A. cepa. In Earwig Nymphs bore into the bulb and make cavities which lead to withering of Crop Pests and Stored Grain Pests and Their Management 371 www.AgriMoon.Com plants. As a prevention spray the infested crop with methyl demeton 25 EC 500 ml or Imidacloprid 17.8 SL 100 -125 ml in 700 L of water per ha. As the strong point of this pest lies in its very quick multiplication the insecticidal treatment has to be repeated as soon as aphid population is found to have built again."
    if s in ['Jute','jute']:
        infmsg+="Your crop may be affected by the following: 1. Stem girdling beetle 2. Jute weevil 3. Spodoptera exigua. The adult beetle girdles the stem at two levels before it starts oviposition. This causes withering, drooping and death of the portion above the lower girdle to a length varying from 5 - 50 cm thus resulting in loss of fibre yield."
        precmsg="In protection spray application of phosalone 0.07% or endosulfan 0.07 % at fortnightly interval. The adult weevil excavates a small hole on the stem and oviposits. The grubs tunnel into the pith. Due to damage a gall-like swelling is formed. To protect spray application of phosalone 0.07% or endosulfan 0.07 or cypermethrin 0.005%. The caterpillars, on hatching, gather on the leaf surface, the epidermis of which they eat. At this young stage, they are also in the habit of webbing together either several leaflets or the margin of the same large leaf. In protection collection and destruction of egg masses or you pray application of phosalone 0.07% or endosulfan 0.07% or cypermethrin 0.005%."
    ans.update({'infmsg':infmsg,'precmsg':precmsg})
    return ans

def UploadImage_view(request):
    form=UploadImage()
    context={}
    if request.method=='POST':
        form1=UploadImage(request.POST,request.FILES)
        print("check2")
        if form1.is_valid():
            print("check")
            form1.save()
            con=ImageProcessing(form1.cleaned_data['Uploaded_image'])
            ans={}
            ans['infmsg']=infmsg
            ans['precmsg']=precmsg
            if con['infected']=='Yes':
                print("success")
                ansp=message(form1.cleaned_data['crop_name'],con)
                ans.update({'infmsg':ansp['infmsg'],'precmsg':ansp['precmsg']})
                print(ans['infmsg'])
            context.update({'form':form1,'infmsg':ans['infmsg'],'precmsg':ans['precmsg']})
            return render(request,'QualityCheck/index.html',context)
    context.update({'form':form,'infmsg':infmsg,'precmsg':precmsg})
    return render(request,'QualityCheck/index.html',context)
