clc;clear;
x=0:500:2500;
y=500:20:800;
testwl=500:0.5:800;
temps=[56.2358	53.7333	50.3962	44.2784	40.3851	38.6056
60.581	56.132	53.351	49.7359	43.8959	42.0607
65.9829	58.6414	55.138	47.796	44.5702	45.1264
70.3283	62.9312	56.1459	51.9746	48.081	45.9678
70.8912	64.3284	57.0983	51.4254	48.7557	49.2002
72.1218	67.2831	57.2718	52.6557	50.1531	47.5381
67.6793	65.6217	58.6692	51.5505	50.8832	50.4383
59.2325	64.0706	56.1732	53.2256	51.168	49.7778
46.2807	54.234	55.3462	50.8971	51.7312	50.619
33.1062	45.0638	51.7378	48.2341	49.5135	48.9572
13.0908	25.6048	39.6206	44.9042	47.0177	49.0756
3.92105	9.76068	26.168	35.4559	45.1892	47.9701
0.59093	3.0934	7.265	19.5007	38.9667	44.8065
0.04154	0.8758	4.04599	10.8871	29.9082	37.3053
0.15988	0.71593	1.99525	7.83506	20.7383	29.0809
0.01154	0.3334	1.2792	7.56407	11.1791	21.4681];
[x,y]=meshgrid(x,y);
% figure(1);
% subplot(2,3,1);
% mesh(x,y,temps);
% xlabel('x');
% ylabel('y');

xj=0:100:2400;
yj=500:20:800;
[xj,yj]=meshgrid(xj,yj);
zj=interp2(x,y,temps,xj,yj,'spline');
K = (1/4)*ones(2);
Tsmooth = conv2(zj,K,'same');
Tsmooth(:,end) = Tsmooth(:,end)*2;
% subplot(2,3,2);
% mesh(x,y,temps);hold on
% surf(xj,yj,Tsmooth);
% xlabel('x');
% ylabel('y');

xi=0:0.5:2400;      %Finial Para Gate Voltage
yi=500:0.05:800;     %Finial Spetrum Wave Length
[xi,yi]=meshgrid(xi,yi);
zi=interp2(xj,yj,Tsmooth,xi,yi,'cubic');
% subplot(2,3,3);
% surf(xi,yi,zi);
% shading interp
% xlabel('x');
% ylabel('y');

xt = 500:0.05:800;
yt = 100*normpdf(xt, 700, 10);%+100*normpdf(xt,744.3, 10);
z0 = zi.';
Vt = z0*yt.';
% subplot(2,3,4);
% plot(xi.',Vt.');
load invs
invs = pinv(z0);

St_m=[];    %Initialize the test spectrum matrix
Vt_m=[];    %Initialize the response IV matrix
split=0:0.02:4;
CenterL = 725;
sigma = 2;

for i=500:0.2:800
    for s = 0.1%[0.1 0.2 0.4 0.7 1 2 4 7 10 20 40 70]
        yt = (1/4)*(s/0.1)*100*normpdf(xt, i, s);
        Vti = z0*yt.';
        St_m = [St_m yt.'];
        Vt_m = [Vt_m Vti];
    end
end
% for i=split
%     yt = 100*normpdf(xt, CenterL-i, sigma)+100*normpdf(xt, CenterL+i, sigma);
%     Vti = z0*yt.';
%     St_m = [St_m yt.'];
%     Vt_m = [Vt_m Vti];
% end

% for i=-8:0.1:3
%     yt = 10^i*normpdf(xt, CenterL, sigma);
%     Vti = z0*yt.';
%     St_m = [St_m yt.'];
%     Vt_m = [Vt_m Vti];
% end
save(strcat('G:\Users\iCalculate\Desktop\Matlab\Database\Retest\','St_s',num2str(s*10),'A_i100_d2A'), 'St_m');
save(strcat('G:\Users\iCalculate\Desktop\Matlab\Database\Retest\','Vt_s',num2str(s*10),'A_i100_d2A'), 'St_m');


%-- Vt_m add noise --%
[a b] = size(Vt_m);
V = 0:0.5:2400;
Amp = repmat(exp(V/2500).',1,b);
noise = wgn(a,b,20).*Amp;
Vt_m_n = Vt_m+0.1*noise;
% subplot(2,3,6);
% mesh(Vt_m_n);
save(strcat('G:\Users\iCalculate\Desktop\Matlab\Database\Retest\','Vn_s',num2str(s*10),'A_i100_d2A'), 'St_m');
%%
subplot(2,3,5);
plot(xt,yt);
hold on
plot(xt,invs*Vti)

%%
subplot(2,3,6);
anser = invs*Vt_m;
[a_max,p] = max(anser,[],2);
norm = anser./a_max;
mesh(norm)
hold on;
plot3(p,[0:300],ones(301),'r.','markersize',30);
axis([0 600 0 300]);

