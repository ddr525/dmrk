                 {РАСЧЁТ МЕТОДИЧЕСКОЙ ПЕЧИ LPC-1700}
                        {составил Изотов Б.В.}
Program FurnaceLab;
 Uses Crt,Graph;
Const
  Em=0.8; Edg=0.36; Ef=0.7; Esio=0.7;
  kSv1=0.15; {Коэффициент смешения газов в I сварочной зоне}
Type
  mas=array[1..100,1..2] of real;
Var
  a,       {Ширина сляба,м}
  alfa,    {Суммарный коэффициент теплоотдачи на поверхность сляба,Вт/(м^2*K)}
  alfa_2,  {Коэффициент конвективной теплоотдачи от футеровки в окр. ср.,-"-}
  bb,      {Длина сляба,м}
  B,       {Расход газа на печь,м^3/cек}
  B_ud,    {Удельный расход газа,м^3/т}
  B_Np,    {Расход газа в зоне нижнего подогрева,м^3/сек}
  B_Sv1,   {Расход топлива в первой сварочной зоне,м^3/сек}
  B_Sv2,   {Расход топлива во второй сварочной зоне,м^3/сек}
  B_Tom,   {Расход топлива в томильной зоне,м^3/сек}
  Bi,      {Aналог числа Био,[-]}
  Ccp,     {Средняя теплоёмкость металла,Дж/кг, а также их сумма}
  Cg,      {Cредняя теплоёмкость смешаного газа,Дж/(м^3*К)}
  Cv,      {Средняя теплоёмкость воздуха,Дж/(м^3*К)}
  dtime,   {Шаг по времени,сек}
  dTk,     {Конечный перепад температур,^C}
  dTmax,   {Максимально допустимый перепад температур,^C}
  dV,      {Элементарный объём,м^3}
  dx,      {Шаг по координате,м}
  Epr,     {Приведенный коэффициент излучения на металл, Вт/(м^2*K^4)   }
  Fmet,Fsv1,Fsv2,Ftom,{Площади футеровки по зонам,м^2}
  fmin,fpl,{Аналоги чисел Фурье,[-]}
  G,       {Производительность печи,кг/сек}
  k1,k2,k3,k4,k5,{Коэффициенты прироста температуры печи,К/cек}
  Ld,      {Действительный расход воздуха,м^3/м^3}
  LsioMet, {Суммарная длина труб СИО в методической зон,м}
  LsioSv1, {Суммарная длина труб СИО в первой сварочной зоне,м}
  LsioSv2, {Суммарная длина труб СИО во второй зоне зоне,м}
  LsioTom, {Суммарная длина труб СИО в томильной зоне,м}
  Lp,      {Длина печи,м}
  Mslab,   {Масса сляба,м}
  Nsteps,  {Количество слябов в печи-количество шагов делаемых одним слябом}
  N2,H2O,O2,CO2, {Cостав дыма,%}
  t1,      {Температура внутренней поверхности футеровки}
  t2,      {Температура между слоями футеровки}
  t3,      {Температура внешней поверхности футеровки}
  td,      {Действительная температура дыма,^C}
  tg,      {Температура подогрева газа,К}
  time,    {Текущее время,сек}
  time_H,  {Время нагрева металла в печи,сек}
  time_H1,time_H2, {Диапазон, в котором ищется время нагрева,сек}
  timeMet,timeSv1,timeSv2,timeTom,  {Время нагрева в каждой зоны,сек}
  Tcpm,    {Cреднемассовая температура нагрева металла на выдаче, K}
  Tmn,     {Начальная температура металла,К}
  Tmk,     {Конечная температура металла,К}
  toc,     {Температура окружающей среды,К}
  Ts,      {Цена смешаного газа}
  tv,      {Температура подогрева воздуха,K}
  tw,      {Текущая температура печи,К}
  TwMetn,TwSv1n,twSv2,twTom,  {Температуры печи по зонам,К}
  twMetNpk,twMetNpk_,twNp,twNp2k,twNp2n,{Температуры в зонах
                                                         нижнего подогрева}
  TwMetn_, {Вспомогательная температура,К}
  v,       {Удельный выход дыма,м^3/м^3}
  w,       {Коэффициент характеризующий степень развития кладки,
                                                           w=Fобщ/Fметалла}
  p,       {Периметр внутренего поперечного сечения кладки,м}
  Q,       {Низшая рабочая теплота сгорания}
  Q_,      {Химическое тепло топлива,%}
  Qd,      {Тепло уходящее из печи с дымом,Вт}
  Qd_,     {Тепло уходящее с дымом,%}
  Qd_Np2_ud,{Тепло уходящее с дымовыми газами из зоны нижнего
                                                          подогрева,Дж/м^3}
  Qd_Np2,
  Qd_Sv1,  {Тепло уходящее с дымовыми газами из первой сварочной,Вт}
  Qd_Sv2,  {Тепло уходящее с дымовыми газами из второй сварочной,Вт}
  Qd_Tom,  {Тепло уходящее с дымовыми газами из томильной зоны,Вт}
  Qd_Sv1_ud,  {Тепло уходящее с дымовыми газами из первой сварочной,Дж/м^3}
  Qd_Sv2_ud,  {Тепло уходящее с дымовыми газами из второй сварочной,Дж/м^3}
  Qd_Tom_ud,  {Тепло уходящее с дымовыми газами из томильной зоны,Дж/м^3}
  Ql,      {Потери тепла через СИО,Вт/м}
  Qm,         {Тепло поглощаемое металлом за весь период нагрева,Вт}
  Qm_ud,dQm,  {Тепло поглощаемое металлом,Дж/кг}
  Qm_ud1,Qm_ud2,dQm1,dQm2,
  Qm_,     {Тепло поглощаемое металлом,%}
  QmMet,QmSv1,QmSv2,QmTom,QmNp1,QmNp2,QmNpMet,QmNpSv1, {Мощность нагрева
                                                       металла по зонам,Вт}
  Qsio_,   {Тепло, теряемое через СИО,%}
  QsioMet, {Тепло, теряемое через СИО в методической зоне,Вт}
  QsioSv1, {Тепло, теряемое через СИО в первой сварочной зоне,Вт}
  QsioSv2, {Тепло, теряемое через СИО во второй сварочной зоне,Вт}
  QsioTom, {Тепло, теряемое через СИО в томильной зоне,Вт}
  Qpr,     {Приход тепла,Вт}
  Qr,      {Расход тепла,Вт}
  Qtr_,    {Тепло транзитных газов,%}
  Qtr_Met, {Тепло газов проходящих через методическую зону транзитом,Вт}
  Qtr_Sv1, {Тепло газов проходящих через первую сварочную зону транзитом,Вт}
  Qtr_Sv2, {Тепло газов проходящих через вторую сварочную зону транзитом,Вт}
  Qf,      {Потери тепла теплопроводностью через футеровку,Вт/м^2}
  Qf_,     {Потери тепла теплопроводностью через футеровку,%}
  QfMet,QfSv1,QfSv2,QfTom,{Потери через футеровку по зонам,Вт}
  Qfv,     {Физическое тепло воздуха,Дж/м^3 газа}
  Qfv_,    {Физическое тепло воздуха,%}
  Qft,     {Физическое тепло газа,Дж/м^3}
  Qft_,    {Физическое тепло топлива,%}
  Qwindow_,{Потери тепла излучением через окно посада или выдачи,%}
  QwindowTom,{Потери тепла излучением через окно выдачи,Вт}
  QwindowMet,{Потери тепла излучением через окно посада,Вт}
  s,       {Толщина сляба,м}
  j,       {Вспомогательная переменная}
  dtdop,   {Допустимый перепад температур,^C}
  tcp,     {Средняя температура слоя,K}
  x_       {Доля проиродного газа в смеси}
  :real;
  t:mas;   {Массив температур по слоям для k-го и (k+1)-го момента времени,К}
  tx:array[1..100,1..4] of real;{Массив температур по слоям для характерных
                   моментов времени (границы зон),K}
  twG,twnG,tmvG,tmnG,tmcG:array[1..700] of real;
           {Изменение характеных температур во времени,K}
  n,       {Кол-во узлов от верхней до нижней поверхности сляба}
  i,       {Cчётчик цикла}
  ss,
  nn,nnSv1,nnSv2,nnMet,k:integer;
  Err,grD,grM:integer;
  ww:text;
Label
  label2,
  labelb;
Function Lambda(g:real):real;{Коэффициент теплопроводности металла,Вт/(м*К)}
  begin
    g:=g-273;
    lambda:=-8e-7*g*g-1.477e-2*g+46.585;
   end;
Function Ro(g:real):real;    {Плотность металла,кг/м^3)}
  begin
    g:=g-273;
    ro:=(7.824-3.355e-4*g)*1000;
  end;
Function C(g:real):real;     {Истиная теплоёмкость металла,Дж/(кг*К)}
  begin
    g:=g-273;
 {   writeln('                  ',g);}
    if g>700 then c:=1618-0.8025*g
             else c:=(0.6938-0.002325*g+4.571e-6*g*g)*1000;
  end;
Function Cd(g:real):real;    {Cредняя теплоёмкость дымовых газов,Дж/(м^3*К)}
Var
  dh2o,do2,dn2,dco2      {Средние теплоёмкости составляющих дыма,кДж/(м^3/К}
  :real;
  begin
     dh2o:=-3.94E-8*g*g+3.795E-4+1.3033;
     do2:=-1.7E-8*g*g+1.495E-4+1.3173;
     dn2:=-2.48E-8*g*g+1.788E-4*g+1.2048;
     dco2:=-7.08E-8*g*g+4.64E-4*g+1.7341;
     cd:=(dh2o*h2o+dco2*co2+dn2*n2+do2*o2)/100*1000;
  end;
Procedure Scr;
Var
ys,xs,ss:integer;
begin
  randomize;
  for ys:=0 to 480 do
  for xs:=0 to 640 do
       begin
         if random(1000)>=500 then ss:=2
                              else ss:=10;
         setcolor(ss);
         if random(1000)>={65}0 then PutPixel(xs,ys,ss);
{         circle(x,y,round(50)); }
       end;
end;

Procedure Ins;
 begin
   if k=1 then OutTextXY(190,30+150,'О программе');
   if k=2 then OutTextXY(214,60+150,'Параметры');
   if k=3 then OutTextXY(250,90+150,'Расчёт');
   if k=4 then OutTextXY(262,120+150,'Выход');
 end;


Procedure Screen;
Var is,as:integer;
cs:char;
label lab1;
begin

clrscr;
grD:=Detect;
InitGraph(grD,grM,'c:\egavga.bgi');
Err:=GraphResult;
if Err=grOk then
 begin
 Scr;
for is:=100 to 500 do
  begin
    sound(is);
    delay(4);
  end;
NoSound;
as:=87;

SetTextStyle(0,HorizDir,3);
outtextxy(35+1,190+1,'Расчёт методической печи');
outtextxy(35-1,190-1,'Расчёт методической печи');
outtextxy(35-1,190+1,'Расчёт методической печи');
outtextxy(35+1,190-1,'Расчёт методической печи');

OutTextXY(35+1,230+1,'стана 1700');
OutTextXY(35-1,230-1,'стана 1700');
OutTextXY(35+1,230-1,'стана 1700');
OutTextXY(35-1,230+1,'стана 1700');
SetColor(4);
SetTextStyle(0,HorizDir,3);
outtextxy(35,190,'Расчёт методической печи');
OutTextXY(35,230,'стана 1700');
{line(320,0,320,480);
line(a,0,a,480);
line(640-a,0,640-a,480); }
repeat
until KeyPressed;





Scr;
for i:=100 to 500 do
  begin
    sound(i);
    delay(4);
  end;
NoSound;

SetTextStyle(0,HorizDir,3);
{a:=262;}
SetColor(0);
OutTextXY(190+1,30+150+1,'О программе');
SetColor(0);
OutTextXY(214+1,60+150+1,'Параметры');
OutTextXY(250+1,90+150+1,'Расчёт');
OutTextXY(262+1,120+150+1,'Выход');

SetColor(0);
OutTextXY(190-1,30+150-1,'О программе');
SetColor(0);
OutTextXY(214-1,60+150-1,'Параметры');
OutTextXY(250-1,90+150-1,'Расчёт');
OutTextXY(262-1,120+150-1,'Выход');

SetColor(0);
OutTextXY(190-1,30+150+1,'О программе');
SetColor(0);
OutTextXY(214-1,60+150+1,'Параметры');
OutTextXY(250-1,90+150+1,'Расчёт');
OutTextXY(262-1,120+150+1,'Выход');

SetColor(0);
OutTextXY(190+1,30+150-1,'О программе');
SetColor(0);
OutTextXY(214+1,60+150-1,'Параметры');
OutTextXY(250+1,90+150-1,'Расчёт');
OutTextXY(262+1,120+150-1,'Выход');

SetColor(4);
OutTextXY(190,30+150,'О программе');
SetColor(2);
OutTextXY(214,60+150,'Параметры');
OutTextXY(250,90+150,'Расчёт');
OutTextXY(262,120+150,'Выход');

k:=1;
if readkey<>'' then
repeat
begin
{if readkey<>'' then }cs:=ReadKey;
if ord(cs)=72 then
            begin
              SetColor(2);
              ins;
              k:=k-1;
            end;
if ord(cs)=80 then
            begin
              SetColor(2);
              ins;
              k:=k+1;
            end;
if k=0 then k:=4;
if k=5 then k:=1;
SetColor(4);
ins;
end;
until ord(cs)=13;
If k=4 then goto lab1;
{  for y:=0 to 480 do
  for x:=0 to 640 do
     PutPixel(x,y,10); }
Scr;
for i:=100 to 500 do
  begin
    sound(i);
    delay(4);
  end;
NoSound;
SetTextStyle(0,HorizDir,3);
SetColor(0);
if k=1 then
  begin

    OutTextXY(190+1,20+1,'О программе');
    OutTextXY(190-1,20-1,'О программе');
    OutTextXY(190+1,20-1,'О программе');
    OutTextXY(190-1,20+1,'О программе');
    SetColor(4);
    OutTextXY(190,20,'О программе');
    SetTextStyle(0,HorizDir,2);
    SetColor(0);
    {OutTextXY(10,240,'  Печь-четырёхзонная методическая толка-');
    OutTextXY(10,270,'тельная с инжекционными горелками.');}
    OutTextXY(10,240+10,'  Модель печи состоит из моделей: ');
    OutTextXY(10,270+10,'-нагрева металла;');
    OutTextXY(10,300+10,'-горения топлива;');
    OutTextXY(10,330+10,'-футеровки;');
    OutTextXY(10,360+10,'-системы испарительного охлаждения;');
    OutTextXY(10,390+10,'-расчёта теплового баланса.');
    repeat
    until readkey<>'';
    screen;
    SetColor(0);
    OutTextXY(10,30,'  Модель нагрева металла построена  на');
    OutTextXY(10,60,'основе явной конечно-разностной  схемы');
    OutTextXY(10,90,'(ЯРС)  и учитывает зависимосить тепло-');
    OutTextXY(10,120,'физических свойств  от  температуры  и');
    OutTextXY(10,150,'несимметричность нагрева слябов по вы-');
    OutTextXY(10,180,'соте.');

  end;

if readkey<>'' then
repeat
until KeyPressed;
Lab1:
closegraph;
end
else
writeln('ошибка',GraphErrorMsg(Err));





CloseGraph;
end;

Procedure Graphics;
var
  x,y:integer;
begin
  SetBkColor(0);
  SetColor(8);
    y:=round((640-nn)/2)-130;
  For x:=0 to 15 do
    line(120+y,430-25*x,nn+120+y,430-25*x);
    line(120+y,55,120+y,430);
    line(120+nn+y,55,120+nn+y,430);
    SetColor(8);
    SetTextStyle(0,HorizDir,1);
    OutTextXY(117+y,435,'0    20   40   60   80  100  120  140  160  180  200  220  240');
    OutTextXY(110+y,427,'0');
    OutTextXY(94+y,427-25,'100');
    OutTextXY(94+y,427-50,'200');
    OutTextXY(94+y,427-75,'300');
    OutTextXY(94+y,427-100,'400');
    OutTextXY(94+y,427-125,'500');
    OutTextXY(94+y,427-150,'600');
    OutTextXY(94+y,427-175,'700');
    OutTextXY(94+y,427-200,'800');
    OutTextXY(94+y,427-225,'900');
    OutTextXY(86+y,427-250,'1000');
    OutTextXY(86+y,427-275,'1100');
    OutTextXY(86+y,427-300,'1200');
    OutTextXY(86+y,427-325,'1300');
    OutTextXY(86+y,427-350,'1400');
    OutTextXY(94+y,427-375,'^C');
    SetTextStyle(0,VertDir,2);
    OutTextXY(80+y,100,'Температура,^C');
    SetTextStyle(0,HorizDir,2);
    OutTextXY(250+y,450,'Время нагрева, мин');
    OutTextXY(-15+y+140,20,'Температурный режим нагрева');
  for i:=1 to 12 do
      begin
        line(round(i*40.1105)+120+y,55,round(i*40.1105)+120+y,430);
      end;
  for i:=1 to (nn-1) do
      begin
        SetColor(6); {печи низ}
        line(i+120+y,431-round(twnG[i]/4),i+1+120+y,430-round(twnG[i+1]/4));
        SetColor(4); {печи верх}
        line(i+120+y,431-round(twG[i]/4),i+1+120+y,430-round(twG[i+1]/4));
        SetColor(3); {металла низ}
        line(i+120+y,431-round(tmnG[i]/4),i+1+120+y,430-round(tmnG[i+1]/4));
        SetColor(5); {металла центр}
        line(i+120+y,431-round(tmcG[i]/4),i+1+120+y,430-round(tmcG[i+1]/4));
        SetColor(2); {металла верх}
        line(i+120+y,431-round(tmvG[i]/4),i+1+120+y,430-round(tmvG[i+1]/4));
     end;
      SetColor(15);
  readln;
end;

Procedure StCh;              {Определение приведенной степени черноты}
  begin
{    Epr:=5.67e-8*Em*Edg*((1-Edg)/w+1)/
    ((1-Edg)/Edg*(Em+Edg*(1-em))/w+1);}

   Epr:=5.67e-8*Em*Edg*((1-Edg)/w+1)/
    ((1-Edg)*(Em+Edg*(1-em))/w+Edg);
{ writeln(Epr:10:10);
    readln;}
  end;

Procedure Burn;    {Расчёт горения топлива}
 var
    aa:array[1..11,1..2] of real;
    bb:array[1..11] of real;
    Cch4,Cc2h6,Cc3h8,Cc4h10,Cc5h12,   {Средние объёмные теплоём-}
    Cco,Ch2,Cco2,Cn2,Co2x,Ch2o,       {кости газов, кДж/(м^3*К) }
    d1,d2,            {Влагосодержание,г/м^3}
    H,Hk,             {Энтальпии дыма,Дж/м^3}
    L0,               {Теоретический расход воздуха,м^3/м^3}
    Npir,             {Пирометрический коэффициент}
    t1,t2,            {Диапазон температур}
    vo2,
    vo2i,vco2,vn2,vh2o,
    Rog,              {Плотность газа при нормальных условиях,кг/м^3}
    Qdg,              {Низшая рабочая теплота сгорания ДГ,Дж/м^3}
    Qng,              {Низшая рабочая теплота сгорания ПГ,Дж/м^3}
    tk,x,y:real;
    n,m:integer;
 label
    l1;
 Begin
    ClrScr;
    textcolor(2);
    writeln('               РАСЧЁТ ГОРЕНИЯ ТОПЛИВА');
         {ПГ-Курдюмовское
         месторождение}         {ДГ}
         aa[1,1]:=98.2;         aa[1,2]:=0.6;        {CH4}
         aa[2,1]:=0.8;          aa[2,2]:=0;          {C2H6}
         aa[3,1]:=0;            aa[3,2]:=0;          {C3H8}
         aa[4,1]:=1.0;          aa[4,2]:=0;          {C4H10}
         aa[5,1]:=0;            aa[5,2]:=0;          {C5H12}
         aa[6,1]:=0;            aa[6,2]:=26;         {CO}
         aa[7,1]:=0;            aa[7,2]:=4.2;        {H2}
         aa[8,1]:=0;            aa[8,2]:=12.2;       {CO2}
         aa[9,1]:=0.0;          aa[9,2]:=57.0;       {N2}
         aa[10,1]:=0;           aa[10,2]:=0;         {O2}
         d1:=10;                d2:=60;              {влагосодержание, г/м^3}
         aa[11,1]:=100*d1/(805+d1);                  {H2O}
         aa[11,2]:=100*d2/(805+d2);                  {H2O}

          for m:=1 to 10 do        {Пересчёт на влажное топливо}
              begin
                aa[m,1]:=aa[m,1]*(1-0.01*aa[11,1]);
                aa[m,2]:=aa[m,2]*(1-0.01*aa[11,2]);
              end;
       Qng:=(358*aa[1,1]+636*aa[2,1]+913*aa[3,1]+1185*aa[4,1]+
             1465*aa[5,1]+127.7*aa[6,1]+108*aa[7,1])*1000;
{             writeln(Qng:5:0);}
        Qdg:=(358*aa[1,2]+636*aa[2,2]+913*aa[3,2]+1185*aa[4,2]+
             1465*aa[5,2]+127.7*aa[6,2]+108*aa[7,2])*1000;
{             writeln(Qdg:5:0);  }
      tv:=350+273;  {т-рa подогрева воздуха,^C}
      tg:=20+273;   {т-рa подогрева газа,^C}
      Npir:=0.725;  {пирометрический коэффициент}

      Cv:=(0.21*(6.5929E-8*tv*tv+1.137E-4*tv+1.2699)+
          0.79*(1.2058E-7*tv*tv-6.0312E-5*tv+1.3012))*1000;

      Cch4:=6.497E-7*tg*tg+5.6125E-4*tg+1.3474;
      Cc2h6:=-5.755E-7*tg*tg+3.273E-3*tg+1.3594;
      Cc3h8:=-2.44329E-6*tg*tg+6.506E-3*tg+1.4532;
      Cc4h10:=0.00054617*tg+2.637;
      Cc5h12:=0.0066452*tg+3.3149;
      Cco:=0.000075*tg+1.273;
      Ch2:=0.0000608*tg+1.2604;
      Cco2:=-5.653E-7*tg*tg+1.3528E-3*tg+1.2726;
      Cn2:=1.2058E-7*tg*tg-6.0312E-5*tg+1.3012;
      Co2x:=6.5929E-8*tg*tg+1.137E-4*tg+1.2699;
      Ch2o:=0.000166*tg+1.449;

    x:=7.1;    {Доля природного газа,%}
    x_:=x/100;
    y:=100-x; {Доля доменного газа,%}
    Ts:=(800.07*x+16.00*y)/100; {цена смешаного газа,грн}
    writeln('Доля природного газа                    ',x:3:1,'%');
    writeln('Доля доменного газа                     ',y:3:1,'%');
    writeln('Цена смешаного газа                     ',Ts:0:2,' грн/1000м^3');
        for m:=1 to 11 do     {Состав смешанного газа,%}
             bb[m]:=(aa[m,1]*x+aa[m,2]*y)/100;
              {Низшая рабочая теплота сгорания смешаного газа}
        Q:=(358*bb[1]+636*bb[2]+913*bb[3]+1185*bb[4]+
             1465*bb[5]+127.7*bb[6]+108*bb[7])*1000;
        Rog:=(0.717*bb[1]+1.357*bb[2]+2.019*bb[3]+2.672*bb[4]+
             3.219*bb[5]+1.251*bb[6]+0.090*bb[7]+1.977*bb[8]+
             1.251*bb[9]+1.429*bb[10]+0.804*bb[11])/100;
        writeln('Низшая рабочая теплота сгорания ПГ     ',(Qng/1000/4.19/293*273):5:0,' ккал/м^3  (при 20^C)');
        writeln('Низшая рабочая теплота сгорания ДГ    ',(Qdg/1000/4.19/293*273):5:0,'  ккал/м^3  (при 20^C)');
        writeln('Низшая рабочая теплота сгорания смеси  ',(Q/1000/4.19/293*273):5:0,' ккал/м^3  (при 20^C)');
        writeln('Плотность газа при н.у.                 ',Rog:5:3,' кг/м^3');
              {Удельный расход воздуха}
        vo2:=0.01*(2*bb[1]+3.5*bb[2]+5*bb[3]+6.5*bb[4]+
             8*bb[5]+0.5*bb[6]+0.5*bb[7]-bb[10]);
        l0:=vo2/0.21;
        ld:=l0*1.05;
        writeln('Действительный расход воздуха          ',ld:5:2,' м^3/м^3');
              {Удельный выход и состав дыма}
        vco2:=0.01*(bb[6]+bb[1]+2*bb[2]+3*Bb[3]+4*bb[4]+5*bb[5]+2*bb[8]);
        vh2o:=0.01*(bb[7]+2*bb[1]+4*bb[3]+5*bb[4]+6*bb[5]+bb[11]);
        vn2:=0.01*bb[9]+0.79*ld;
        vo2i:=0.01*bb[10]+0.0105*l0;
        v:=vco2+vh2o+vn2+vo2i;
        writeln('Удельный выход дыма                    ',v:5:2,' м^3/м^3');
        v:=v*0.01;
        write('Состав дыма:');
        co2:=vco2/v;
        n2:=vn2/v;
        h2o:=vh2o/v;
        o2:=vo2i/v;
        v:=v*100;
        writeln(' CO2=',co2:3:1,'%');
        writeln('             N2=',n2:3:1,'%');
        writeln('             H2O=',h2o:3:1,'%');
        writeln('             O2=',o2:3:1,'%');
              {Теплоёмкость cмешаного газа}
        cg:=(Cch4*bb[1]+Cc2h6*bb[2]+Cc3h8*bb[3]+Cc4h10*bb[4]+Cc5h12*bb[5]+
            Cco*bb[6]+Ch2*bb[7]+Cco2*bb[8]+Cn2*bb[9]+Co2x*bb[10]+
            Ch2o*bb[11])/100*1000;
        Qft:=cg*(tg-273);      {Физическое тепло топлива}
        Qfv:=ld*cv*(tv-273);   {Физическое тепло воздуха}
          Hk:=(q+qfv+qft)/v;
          t1:=500;
          t2:=3500;
      l1:     tk:=(t1+t2)/2;
              H:=cd(tk)*(tk-273);
              if H<Hk then t1:=tk else t2:=tk;
         if (H<0.999*Hk)or(H>1.001*Hk) then goto l1;
         td:=(tk-273)*Npir;
         writeln('Теплоёмкость дыма                     ',cd(tk):6:0,' кДж/(м^3*К)');
         writeln('Калориметрическая температура         ',tk:6:0,'^C');
         writeln('Действительная температура            ',td:6:0,'^C');
    {    readln;  }
        readln;
        writeln;
 end;

Procedure Temp1;
  begin
    j:=T[n,1];
    alfa:=Epr*(tw*tw*tw*tw-j*j*j*j)/(Tw-j)+40;
    Bi:=alfa*dx/lambda(0.5*(t[n-1,1]+t[n,1]));
    fmin:=lambda((t[n,1]+t[n-1,1])/2)*dtime/c(t[n,1])/ro(t[n,1])/dx/dx;
    if fmin>0.5/(1+Bi) then writeln('sx neust');
    t[n,2]:=2*fmin*t[n-1,1]+(1-2*fmin*(1+Bi))*t[n,1]+2*fmin*Bi*tw;
  end;
Procedure Temp2;
var
  rr,
  tmin:real;
  Nmin:integer;
  begin
    for i:=(n-1) downto 2 do
      begin
         fmin:=lambda((t[i,1]+t[i-1,1])/2)*dtime/c(t[i,1])/ro(t[i,1])/dx/dx;
         fpl:=lambda((t[i,1]+t[i+1,1])/2)*dtime/c(t[i,1])/ro(t[i,1])/dx/dx;
         t[i,2]:=t[i,1]+fpl*(t[i+1,1]-t[i,1])-fmin*(t[i,1]-t[i-1,1]);
      end;
         fpl:=lambda((t[1,1]+t[2,1])/2)*dtime/c(t[1,1])/ro(t[1,1])/dx/dx;
    {t[1,2]:=t[1,1]*(1-2*fpl)+2*fpl*t[2,1];}
     j:=T[n,1];
    alfa:=Epr*(twNp*twNp*twNp*twNp-j*j*j*j)/(TwNp-j)+40;
    Bi:=alfa*dx/lambda(0.5*(t[2,1]+t[1,1]));
    fmin:=lambda((t[1,1]+t[2,1])/2)*dtime/c(t[1,1])/ro(t[1,1])/dx/dx;
    if fmin>0.5/(1+Bi) then writeln('sx neust');
    t[1,2]:=2*fmin*t[2,1]+(1-2*fmin*(1+Bi))*t[1,1]+2*fmin*Bi*twNp;

    if (t[n,2]-t[trunc(n/2),2])>dtmax then
                  dtmax:=t[n,2]-t[trunc(n/2),2];
    {определение энтальпии металла}
        dQm:=0;
    for i:=1 to (n-1) do
        begin
          tcp:=(t[i,2]+t[i+1,2])/2;
          dQm:=dQm+c(tcp)*(t[i,2]-t[i,1])/(n-1);
          ccp:=ccp+c(tcp);
        end;
        Qm_ud:=Qm_ud+dQm;
         nmin:=round(n/2);
            dQm1:=0;
    for i:=1 to (nmin-1) do
        begin
          tcp:=(t[i,2]+t[i+1,2])/2;
          dQm1:=dQm1+c(tcp)*(t[i,2]-t[i,1])/(nMin-1)/2{*(nmin)/n};
        end;
        Qm_ud1:=Qm_ud1+dQm1;

        dQm2:=0;
    for i:=Nmin to (n-1) do
        begin
          tcp:=(t[i,2]+t[i+1,2])/2;
          dQm2:=dQm2+c(tcp)*(t[i,2]-t[i,1])/(n-Nmin)/2{*(n-nmin)/n};
        end;
        Qm_ud2:=Qm_ud2+dQm2;
    if time=600*trunc(time/600) then
         begin
          {  writeln(ww,'  time=',time:6{,'час');
              {    for i:=1 to n do
                      writeln(ww,'t[',i,']=');
                      writeln(ww,';');
                  for i:=1 to n do
                      writeln(ww,(t[i,2]-273):5:0);
                      writeln(ww,';');  }
          {  writeln(ww,{'Тпечи=',}{(tw-273):5:1{,'^C'}{);
            writeln(ww,}{'Tпов=',}{(t[n,1]-273):5:1{,'^C'}{);
            writeln(ww,'Тц=',(t[1,1]-273):5:1,'^C');
           { writeln;
            readln; }
         end;
    for i:=1 to n do
       t[i,1]:=t[i,2];
  end;

Procedure Temp3;
var
  rr,
  tmin:real;
  Nmin:integer;
  begin
    for i:=(n-1) downto 2 do
      begin
         fmin:=lambda((t[i,1]+t[i-1,1])/2)*dtime/c(t[i,1])/ro(t[i,1])/dx/dx;
         fpl:=lambda((t[i,1]+t[i+1,1])/2)*dtime/c(t[i,1])/ro(t[i,1])/dx/dx;
         t[i,2]:=t[i,1]+fpl*(t[i+1,1]-t[i,1])-fmin*(t[i,1]-t[i-1,1]);
      end;
         fpl:=lambda((t[1,1]+t[2,1])/2)*dtime/c(t[1,1])/ro(t[1,1])/dx/dx;
    {t[1,2]:=t[1,1]*(1-2*fpl)+2*fpl*t[2,1];}
     j:=T[n,1];
    alfa:=0;
    Bi:=alfa*dx/lambda(0.5*(t[2,1]+t[1,1]));
    fmin:=lambda((t[1,1]+t[2,1])/2)*dtime/c(t[1,1])/ro(t[1,1])/dx/dx;
    if fmin>0.5/(1+Bi) then writeln('sx neust');
    t[1,2]:=2*fmin*t[2,1]+(1-2*fmin*(1+Bi))*t[1,1]+2*fmin*Bi*twNp;

    if (t[n,2]-t[trunc(n/2),2])>dtmax then
                  dtmax:=t[n,2]-t[trunc(n/2),2];
    {определение энтальпии металла}
        dQm:=0;
    for i:=1 to (n-1) do
        begin
          tcp:=(t[i,2]+t[i+1,2])/2;
          dQm:=dQm+c(tcp)*(t[i,2]-t[i,1])/(n-1);
          ccp:=ccp+c(tcp);
        end;
        Qm_ud:=Qm_ud+dQm;
         nmin:=round(n/2);
            dQm1:=0;
    for i:=1 to (nmin-1) do
        begin
          tcp:=(t[i,2]+t[i+1,2])/2;
          dQm1:=dQm1+c(tcp)*(t[i,2]-t[i,1])/(nMin-1)/2{*(nmin)/n};
        end;
        Qm_ud1:=Qm_ud1+dQm1;

        dQm2:=0;
    for i:=Nmin to (n-1) do
        begin
          tcp:=(t[i,2]+t[i+1,2])/2;
          dQm2:=dQm2+c(tcp)*(t[i,2]-t[i,1])/(n-Nmin)/2{*(n-nmin)/n};
        end;
        Qm_ud2:=Qm_ud2+dQm2;
    if time=600*trunc(time/600) then
         begin
          {  writeln(ww,'  time=',time:6{,'час');
              {    for i:=1 to n do
                      writeln(ww,'t[',i,']=');
                      writeln(ww,';');
                  for i:=1 to n do
                      writeln(ww,(t[i,2]-273):5:0);
                      writeln(ww,';');  }
          {  writeln(ww,{'Тпечи=',}{(tw-273):5:1{,'^C'}{);
            writeln(ww,}{'Tпов=',}{(t[n,1]-273):5:1{,'^C'}{);
            writeln(ww,'Тц=',(t[1,1]-273):5:1,'^C');
           { writeln;
            readln; }
         end;
    for i:=1 to n do
       t[i,1]:=t[i,2];
  end;




Procedure Fettling;   {Расчёт футеровки печи}
const
  a1=676.162e-7;  {коэффициент температуропроводности шамотa, м^2/c}
 var
  alfa_1,       {Суммарный коэффициент теплоотдачи на футеровку, Вт/(м^2*К)}
  dst1,dst2,    {толщина стены,м}
  Epr_f,        {Приведенный коэффициент излучения на футеровку, Вт/м^2/K^4)}
  lambda1,
  lambda2,
  t_1,
  t_2,
  tcp1,tcp2,    {Cредние температуры слоёв}
  t2x,
  Qf1
  :real;
label
  label_1,
  label_2;
begin
  dst1:=0.464;
  dst2:=0.115;
  t_1:=toc;
  t_2:=tw;
label_1:
     t1:=(t_1+t_2)/2;
     t2:=(t1+toc)/2;
     Epr_f:=5.67e-8/(1/ef+1/edg-1);
     alfa_1:=Epr_f*(tw*tw*tw*tw-t1*t1*t1*t1)/(Tw-t1)+40;
     Qf:=alfa_1*(tw-t1);
     t3:=Qf/alfa_2+toc;
{writeln('alfa_2=',(alfa_2):5:2);}
   label_2:
        t2x:=t2;
        tcp2:=(t2x+t3)/2;
        lambda2:=(0.84+0.58e-3*(tcp-273));
        t2:=Qf*dst2/lambda2+t3;
        if (t2-t2x)/t2>0.0001 then goto label_2;
     lambda1:=(0.84+0.58e-3*((t1+t2)/2-273))*5;
     Qf1:=lambda1/dst1*(t1-t2);
     if Qf>Qf1 then  t_1:=t1
               else  t_2:=t1;
     if abs(Qf-Qf1)/Qf>0.0001 then goto label_1;
{writeln('t1=',(t1-273):5:2);
writeln('t2=',(t2-273):5:2);
writeln('t3=',(t3-273):5:2);
readln;                     }
end;

Procedure SIO;
var
  alfa_3,
  Epr_s,
  fi,
  lambda3,
  lambda4,
  Ql1,
  r1,r2,r3,
  t_1,t_2,
  tnas,
  tst
  :real;
label
  label5;
begin
  tnas:=180+273;    {при Р=10 МПа}
  r2:=0.146/2;
  r1:=r2-0.030;
  r3:=r2+0.0132;
  w:=p/(pi*r3*2);
  Epr_s:=5.67e-8*Esio*Edg*((1-Edg)/w+1)/
    ((1-Edg)/Edg*(Esio+Edg*(1-Esio))/w+1);
  t_1:=tnas;
  t_2:=tw;
label5:
  tst:=(t_1+t_2)/2;
  j:=tst;
  alfa:=Epr*(tw*tw*tw*tw-j*j*j*j)/(Tw-j)+40;
  lambda3:=30;
  lambda4:=2;
  Ql:=2*pi*(tw-tnas)/(1/alfa_3/R3+ln(r2/r1)/lambda3+ln(r3/r2)/lambda4);
  Ql1:=2*pi*(tst-tnas)/(ln(r2/r1)/lambda3+ln(r3/r2)/lambda4);
  if Ql<Ql1 then t_2:=tst
            else t_1:=tst;
  if abs(Ql-Ql1)/Ql>0.01 then goto label5;
end;
Procedure Balance;
begin
   ClrScr;
   writeln('                 РАСЧЁТ ТЕПЛОВОГО БАЛАНСА');
                                                    textcolor(6);
   writeln('   МЕТОДИЧЕСКАЯ ЗОНА');                 textcolor(8);
     Qr:=QmMet+QfMet+QsioMet+QwindowMet;
     Qtr_Met:=Qr;
     Qpr:=Qtr_Met;
     Qm_:=QmMet/Qr*100;
     Qf_:=QfMet/Qr*100;
     Qsio_:=QsioMet/Qr*100;
     Qwindow_:=QwindowMet/Qr*100;
   writeln('      ПРИХОД ТЕПЛА');                   textcolor(2);
   writeln('Тепло транзитных газов      ',(Qtr_Met/1000000):5:2,' MВт   ',(Qtr_Met/Qpr*100):5:1,' %');
   writeln('Итого приход                ',(Qpr/1000000):5:2,' MВт   ',(Qtr_Met/Qpr*100):5:1,' %');
                                                    textcolor(8);
   writeln('      РАСХОД ТЕПЛА');                   textcolor(2);
   writeln('Тепло на нагрев металла     ',(QmMet/1000000):5:2,' MВт   ',Qm_:5:1,' %');
   writeln('Потери через кладку         ',(QfMet/1000000):5:2,' MВт   ',Qf_:5:1,' %');
   writeln('Потери через СИО            ',(QsioMet/1000000):5:2,' МВт   ',Qsio_:5:1,' %');
   writeln('Потери через окно посада    ',(QwindowMet/1000000):5:2,' МВт   ',Qwindow_:5:1,' %');
   writeln('Итого расход                ',(Qr/1000000):5:2,' MВт   ',(Qm_+Qf_+Qsio_+Qwindow_):5:1,' %');
   readln;
   ClrScr;

   writeln('                 РАСЧЁТ ТЕПЛОВОГО БАЛАНСА');
                                                    textcolor(6);
   writeln('   ПЕРВАЯ СВАРОЧНАЯ ЗОНА');
     Qpr:=(Q+Qfv+Qft)*B_Sv1+Qtr_Sv1;
     Qr:=QmSv1+QfSv1+Qd_Sv1+kSv1*(QsioSv1+QmNpSv1);
     Q_:=Q*B_Sv1/Qpr*100;
     Qfv_:=Qfv*B_Sv1/Qpr*100;
     Qft_:=Qft*B_Sv1/Qpr*100;
     Qtr_:=Qtr_Sv1/Qpr*100;
     Qm_:=(QmSv1+QmNpSv1*kSv1)/Qr*100;
     Qf_:=QfSv1/Qr*100;
     Qsio_:=kSv1*QsioSv1/Qr*100;
     Qd_:=Qd_Sv1/Qr*100;                            textcolor(8);
   writeln('      ПРИХОД ТЕПЛА');                   textcolor(2);
   writeln('Химическое тепло топлива    ',(Q*B_Sv1/1000000):5:2,' MВт   ',Q_:5:1,' %');
   writeln('Физическое тепло воздуха    ',(Qfv*B_Sv1/1000000):5:2,' MВт   ',Qfv_:5:1,' %');
   writeln('Физическое тепло газа       ',(Qft*B_Sv1/1000000):5:2,' MВт   ',Qft_:5:1,' %');
   writeln('Тепло транзитных газов      ',(Qtr_Sv1/1000000):5:2,' MВт   ',Qtr_:5:1,' %');
   writeln('Итого приход                ',(Qpr/1000000):5:2,' MВт   ',(Q_+Qfv_+Qft_+Qtr_):5:1,' %');
                                                    textcolor(8);
   writeln('      РАСХОД ТЕПЛА');                   textcolor(2);
   writeln('Тепло на нагрев металла     ',(QmSv1/1000000):5:2,' MВт   ',Qm_:5:1,' %');
   writeln('Потери через кладку         ',(QfSv1/1000000):5:2,' MВт   ',Qf_:5:1,' %');
   writeln('Тепло уходящее с дымом      ',(Qd_Sv1/1000000):5:2,' MВт   ',Qd_:5:1,' %');
   writeln('Потери через СИО            ',(kSv1*QsioSv1/1000000):5:2,' МВт   ',Qsio_:5:1,' %');
   writeln('Итого расход                ',(Qr/1000000):5:2,' MВт   ',(Qm_+Qf_+Qd_+Qsio_):5:1,' %');
   writeln;
   writeln('Расход топлива               ',(B_Sv1/1000*3600):0:3,'тыс. м^3/час');
   readln;
   ClrScr;
   writeln('                 РАСЧЁТ ТЕПЛОВОГО БАЛАНСА');
                                                    textcolor(6);
   writeln('   ВТОРАЯ СВАРОЧНАЯ ЗОНА');             textcolor(2);
     Qpr:=(Q+Qfv+Qft)*B_Sv2+Qtr_Sv2;
     Qr:=QmSv2+QfSv2+Qd_Sv2{+QsioSv2};
     Q_:=Q*B_Sv2/Qpr*100;
     Qfv_:=Qfv*B_Sv2/Qpr*100;
     Qft_:=Qft*B_Sv2/Qpr*100;
     Qtr_:=Qtr_Sv2/Qpr*100;
     Qm_:=QmSv2/Qr*100;
     Qf_:=QfSv2/Qr*100;
{     Qsio_:=QsioSv2/Qr*100;  }
     Qd_:=Qd_Sv2/Qr*100;                            textcolor(8);
   writeln('      ПРИХОД ТЕПЛА');                   textcolor(2);
   writeln('Химическое тепло топлива    ',(Q*B_Sv2/1000000):5:2,' MВт   ',Q_:5:1,' %');
   writeln('Физическое тепло воздуха    ',(Qfv*B_Sv2/1000000):5:2,' MВт   ',Qfv_:5:1,' %');
   writeln('Физическое тепло газа       ',(Qft*B_Sv2/1000000):5:2,' MВт   ',Qft_:5:1,' %');
   writeln('Тепло транзитных газов      ',(Qtr_Sv2/1000000):5:2,' MВт   ',Qtr_:5:1,' %');
   writeln('Итого приход                ',(Qpr/1000000):5:2,' MВт   ',(Q_+Qfv_+Qft_+Qtr_):5:1,' %');
                                                    textcolor(8);
   writeln('      РАСХОД ТЕПЛА');                   textcolor(2);
   writeln('Тепло на нагрев металла     ',(QmSv2/1000000):5:2,' MВт   ',Qm_:5:1,' %');
   writeln('Потери через кладку         ',(QfSv2/1000000):5:2,' MВт   ',Qf_:5:1,' %');
   writeln('Тепло уходящее с дымом      ',(Qd_Sv2/1000000):5:2,' MВт   ',Qd_:5:1,' %');
{   writeln('Потери через СИО            ',(QsioSv2/1000000):5:2,' МВт   ',Qsio_:5:1,' %');}
   writeln('Итого расход                ',(Qr/1000000):5:2,' MВт   ',(Qm_+Qf_+Qd_):5:1,' %');
   writeln;
   writeln('Расход топлива               ',(B_Sv2/1000*3600):0:3,'тыс. м^3/час');
   writeln;
   readln;

   ClrScr;
   writeln('                 РАСЧЁТ ТЕПЛОВОГО БАЛАНСА');
                                                    textcolor(6);
   writeln('   ТОМИЛЬНАЯ ЗОНА');                    textcolor(2);
     Qpr:=(Q+Qfv+Qft)*B_Tom;
     Qr:=QmTom+QfTom+Qd_Tom{+QsioTom}+QwindowTom;
     Q_:=Q*B_Tom/Qpr*100;
     Qfv_:=Qfv*B_Tom/Qpr*100;
     Qft_:=Qft*B_Tom/Qpr*100;
     Qm_:=QmTom/Qr*100;
     Qf_:=QfTom/Qr*100;
     Qwindow_:=QwindowTom/Qr*100;
{     Qsio_:=QsioTom/Qr*100;}
     Qd_:=Qd_Tom/Qr*100;                            textcolor(8);
   writeln('      ПРИХОД ТЕПЛА');                   textcolor(2);
   writeln('Химическое тепло топлива    ',(Q*B_Tom/1000000):5:2,' MВт   ',Q_:5:1,' %');
   writeln('Физическое тепло воздуха    ',(Qfv*B_Tom/1000000):5:2,' MВт   ',Qfv_:5:1,' %');
   writeln('Физическое тепло газа       ',(Qft*B_Tom/1000000):5:2,' MВт   ',Qft_:5:1,' %');
   writeln('Итого приход                ',(Qpr/1000000):5:2,' MВт   ',(Q_+Qfv_+Qft_):5:1,' %');
                                                    textcolor(8);
   writeln('      РАСХОД ТЕПЛА');                   textcolor(2);
   writeln('Тепло на нагрев металла     ',(QmTom/1000000):5:2,' MВт   ',Qm_:5:1,' %');
   writeln('Потери через кладку         ',(QfTom/1000000):5:2,' MВт   ',Qf_:5:1,' %');
   writeln('Тепло уходящее с дымом      ',(Qd_Tom/1000000):5:2,' MВт   ',Qd_:5:1,' %');
 {  writeln('Потери через СИО            ',(QsioTom/1000000):5:2,' МВт   ',Qsio_:5:1,' %');}
   writeln('Потери через окно выдачи    ',(QwindowTom/1000000):5:2,' МВт   ',Qwindow_:5:1,' %');
   writeln('Итого расход                ',(Qr/1000000):5:2,' MВт   ',(Qm_+Qf_+Qd_+Qwindow_):5:1,' %');
   writeln;
   writeln('Расход топлива               ',(B_Tom/1000*3600):0:3,'тыс. м^3/час');
   readln;
   ClrScr;
      writeln('                 РАСЧЁТ ТЕПЛОВОГО БАЛАНСА');
                                                    textcolor(6);
   writeln('   ЗОНА НИЖНЕГО ПОДОГРЕВА');            textcolor(2);
     Qpr:=(Q+Qfv+Qft)*B_Np;
     Qr:=QmNp2+Qd_Np2+QsioTom+QsioSv2;
     Q_:=Q*B_Np/Qpr*100;
     Qfv_:=Qfv*B_Np/Qpr*100;
     Qft_:=Qft*B_Np/Qpr*100;
     Qm_:=QmNp2/Qr*100;
{     Qf_:=QfTom/Qr*100;}
     Qsio_:=(QsioTom+QsioSv2)/Qr*100;
     Qd_:=Qd_Np2/Qr*100;                            textcolor(8);
   writeln('      ПРИХОД ТЕПЛА');                   textcolor(2);
   writeln('Химическое тепло топлива    ',(Q*B_Np/1000000):5:2,' MВт   ',Q_:5:1,' %');
   writeln('Физическое тепло воздуха    ',(Qfv*B_Np/1000000):5:2,' MВт   ',Qfv_:5:1,' %');
   writeln('Физическое тепло газа       ',(Qft*B_Np/1000000):5:2,' MВт   ',Qft_:5:1,' %');
   writeln('Итого приход                ',(Qpr/1000000):5:2,' MВт   ',(Q_+Qfv_+Qft_):5:1,' %');
                                                    textcolor(8);
   writeln('      РАСХОД ТЕПЛА');                   textcolor(2);
   writeln('Тепло на нагрев металла     ',(QmNp2/1000000):5:2,' MВт   ',Qm_:5:1,' %');
{   writeln('Потери через кладку         ',(QfTom/1000000):5:2,' MВт   ',Qf_:5:1,' %');}
   writeln('Тепло уходящее с дымом      ',(Qd_Np2/1000000):5:2,' MВт   ',Qd_:5:1,' %');
   writeln('Потери через СИО            ',((QsioTom+QsioSv2)/1000000):5:2,' МВт   ',Qsio_:5:1,' %');
   writeln('Итого расход                ',(Qr/1000000):5:2,' MВт   ',(Qm_{+Qf_}+Qd_+Qsio_):5:1,' %');
   writeln;
   writeln('Расход топлива               ',(B_Np/1000*3600):0:3,'тыс. м^3/час');
   readln;

   ClrScr;
   writeln('                 РАСЧЁТ ТЕПЛОВОГО БАЛАНСА');
                                                    textcolor(6);
   writeln('   ТЕПЛОВОЙ БАЛАНС ПЕЧИ');              textcolor(2);
     B:=B_Tom+B_Sv1+B_Sv2+B_Np;
     B_ud:=B/G*1000;
     Qm:=Qm_ud*G;
     Qd:=(B{-B_Np})*v*Cd(twMetn)*(twMetn-273){+B_Np*v*Cd(twNp1n)*(twNp1n-273)};
     Qpr:=B*(Q+Qfv+Qft);
     Qr:=Qm+(QfMet+QfSv1+QfSv2+QfTom)+Qd+(QsioMet+QsioSv1+QsioSv2+QsioTom)
            +QwindowTom+QwindowMet;
     Q_:=B*Q/Qpr*100;
     Qfv_:=B*Qfv/Qpr*100;
     Qft_:=B*Qft/Qpr*100;
     Qm_:=Qm/Qr*100;
     Qsio_:=(QsioMet+QsioSv1+QsioSv2+QsioTom)/Qr*100;
     Qf_:=(QfMet+QfSv1+QfSv2+QfTom)/Qr*100;
     Qd_:=Qd/Qr*100;
     Qwindow_:=(QwindowTom+QwindowMet)/Qr*100;
                                                    textcolor(8);
   writeln('      ПРИХОД ТЕПЛА');                   textcolor(2);
   writeln('Химическое тепло топлива    ',(B*Q/1000000):5:2,' MВт   ',Q_:5:1,' %');
   writeln('Физическое тепло воздуха    ',(B*Qfv/1000000):5:2,' MВт   ',Qfv_:5:1,' %');
   writeln('Физическое тепло газа       ',(B*Qft/1000000):5:2,' MВт   ',Qft_:5:1,' %');
   writeln('Итого приход                ',(Qpr/1000000):5:2,' MВт   ',(Q_+Qfv_+Qft_):5:1,' %');
                                                    textcolor(8);
   writeln('      РАСХОД ТЕПЛА');                   textcolor(2);
   writeln('Тепло на нагрев металла     ',(Qm/1000000):5:2,' MВт   ',Qm_:5:1,' %');
   writeln('Потери через кладку         ',((QfMet+QfSv1+QfSv2+QfTom)/1000000):5:2,' MВт   ',Qf_:5:1,' %');
   writeln('Тепло уходящее с дымом      ',(Qd/1000000):5:2,' MВт   ',Qd_:5:1,' %');
   writeln('Потери через СИО            ',((QsioMet+QsioSv1+QsioSv2+QsioTom)/1000000):5:2,' МВт   ',Qsio_:5:1,' %');
   writeln('Потери излучением ч/з окнa  ',(QwindowTom/1000000):5:2,' МВт   ',Qwindow_:5:1,' %');
   writeln('Итого расход                ',(Qr/1000000):5:2,' MВт   ',(Qm_+Qf_+Qd_+Qsio_+Qwindow_):5:1,' %');
   writeln;
   writeln('Расход топлива                ',(B/1000*3600):0:2,'тыс. м^3/час     ');
   readln;
end;

BEGIN
  { Screen;}

   Burn;

   dtdop:=318;
   n:=10;          {кол-во узлов от верхней до нижней поверхности}
   s:=0.200;        {толщина сляба,м}
   bb:=9.1;       {длина сляба,м}
   a:=1.250;      {ширина сляба,м}
   dx:=s/(n-1);
   dtime:=6;
   toc:=20+273;
{   tmk:=1280+273;}
   time_H:=240*60;      {время нагрева, сек=мин*60}
   twMetn:=1050+273;
   tmn:=20+273;
   twSv1n:=1300+273;   {т-ра 1-ой зоны}
   {холодный посад}
{   tmn:=600+273;
   twSv1n:=1280.8+273; {тёплый посад}
{   tmn:=700+273;
   twSv1n:=943.1+273; {горячий посад}
   twSv2:=1350+273;    {т-ра 3-ей зоны}
   twTom:=1280+273;    {т-ра 5-ой зоны}
{   twNp1n:=763+273;}
   twNp2n:=1250+273; {т-ра 4-ой зоны}
   twNp2k:=1250+273;
   twMetNpk:=1100+273; {т-ра 2-ой зоны}
{   twMetn:=twSv1n-140;  }
   alfa_2:=8+0.05*(toc-273);

   Lp:=35.544;
   Fmet:=31.05+35.99;
   Fsv1:=54.88+49.69;
   Fsv2:=92.7+63.4;
   Ftom:=41.63+51.65;
   LsioMet:=2*4*Lp*0.189+6.708*2*2;
   LsioSv1:=4*Lp*0.245+6.708*2*3;
   LsioSv2:=4*Lp*0.312+6.708*2*4;
   LsioTom:=4*Lp*0.254+6.708*2*2;

   ClrScr;
   for i:=1 to 10 do writeln;
     writeln('                     Подождите.Идёт расчёт нагрева металла');
{Label1:
   time_H1:=0;
   time_H2:=5.44*3600;}


Label2:
{   time_H:=(time_H1+time_H2)/2;}
    timeMet:=time_H*0.1784;
    timeSv1:=time_H*0.2826;
    timeSv2:=time_H*0.2944;
    timeTom:=time_H*0.2446;
{     timeMet:=15*60;
    timeSv1:=27*60;
    timeSv2:=75*60;
    timeTom:=18*60;}
   dV:=dx*bb*dtime*Lp/time_H;
   G:=Lp*bb*s*ro(900)/time_H;
   Mslab:=a*bb*s*ro(900);
   Nsteps:=time_H*G/Mslab;

   ccp:=0;
   Qm_ud:=0;
   Qm_ud1:=0;
   Qm_ud2:=0;

    assign(ww,'c:\ДИПЛОМ\Results\kursWork.xls');
    textcolor(2);

                      {РАСЧЕТ НАГРЕВА МЕТАЛЛА}
   for i:=1 to n do
     t[i,1]:=tmn;
   time:=0;
   dtmax:=0;
   nn:=0;
   ss:=5;
           {НАГРЕВ МЕТАЛЛА В МЕТОДИЧЕСКОЙ ЗОНЕ}
     w:=1.86;
     StCh;
     tw:=(twMetn+twSv1n)/2;
     Fettling;

     p:=(1.680+6.708)*2;
     Sio;

     QsioMet:=Ql*LsioMet;
     QfMet:=Qf*Fmet;

     tw:=twMetn;
     twNp:=twMetn-50;
     while time<=timeMet do
       begin
       { if (time=0)or(time=2*60)or(time=4*60) then
                  begin}
                    tw:=twMetn+(twSv1n-twMetn)*time/timeMet;
                    twNp:=(twMetn-50)+(twMetNpk-(twMetn-50))*time/timeMet;
             {     end;  }
          Temp1;
          Temp2;
  {      Writeln((time/60):5:2,'мин    tw=',tw:5:0,'^C    twNp=',twNp:5:0);
        readln;  }
            if time=ss*round(time/ss) then
                                begin
                                  nn:=nn+1;
                                  twG[nn]:=tw-273;
                                  twnG[nn]:=twNp-273;
                               {   writeln(twnG[nn]:5:2);}
                                  tmnG[nn]:=t[1,2]-273;
                                  tmvG[nn]:=t[n,2]-273;
                                  tmcG[nn]:=t[round(n/2),2]-273;
                                end;
        time:=time+dtime;
       end;
     NNmet:=nn;
     QmMet:=Qm_ud2*G;
     QmNpMet:=Qm_ud1*G;
     for i:=1 to n do
         tx[i,1]:=t[i,1];
           {НАГРЕВ МЕТАЛЛА В ПЕРВОЙ СВАРОЧНОЙ ЗОНЕ}
     w:=2.1;
     StCh;
     tw:=(twSv1n+twSv2)/2;
     Fettling;
     Sio;
     QsioSv1:=Ql*LsioSv1;
     QfSv1:=Qf*Fsv1;
     {k2:=(twSv2-twSv1n)/timeSv1;
     k5:=(twNp2n-twMetNpk)/timeSv1;}
     tw:=twSv1n;
     twNp:=twMetNpk;
     while time<(timeMet+timeSv1)  do
     begin
      { if (time=40*60)or(time=42*60)or(time=44*60)or(time=46*60)
        or(time=80*60)or(time=82*60) then
              begin
                tw:=tw+(twSv2-twSv1n)/7;
                twNp:=twNp+(twNp2n-twMetNpk)/7;    }

                 tw:=twSv1n+(twSv2-twSv1n)*(time-timeMet)/timeSv1;
                 twNp:=twMetNpk+(twNp2n-twMetNpk)*(time-timeMet)/timeSv1;
       {       end;}
       Temp1;
       Temp2;
            if time=ss*round(time/ss) then
                                begin
                                  nn:=nn+1;
                                  twG[nn]:=round(tw-273);
                                  twnG[nn]:=twNp-273;
                                  tmnG[nn]:=t[1,2]-273;
                                  tmvG[nn]:=t[n,2]-273;
                                  tmcG[nn]:=t[round(n/2),2]-273;

                                end;

       time:=time+dtime;
     end;
     NNsv1:=nn;
     QmSv1:=Qm_ud2*G-QmMet;
     QmNp1:=Qm_ud1*G;
     QmNpSv1:=QmNp1-QmNpMet;
     for i:=1 to n do
         tx[i,2]:=t[i,1];
           {НАГРЕВ МЕТАЛЛА ВО ВТОРОЙ СВАРОЧНОЙ ЗОНЕ}
     w:=2.5;
     StCh;
     tw:=twSv2;
{     twNp:=twNpk;  }
     Fettling;
     p:=(1.960+6.708)*2;
     Sio;
     QsioSv2:=Ql*LsioSv2;
     Qfsv2:=Qf*Fsv2;
     k4:=(twNp2k-twNp2n)/(timeSv2+timeTom);
     twNp:=twNp2n;
  while time<(timeMet+timeSv1+timeSv2)  do
     begin
      { twNp:=twNp2n+k4*((time_H/Nsteps*trunc(time*Nsteps/time_H))-timeMet-timeSv1);}
       Temp1;
       Temp2;
            if time=ss*round(time/ss) then
                                begin
                                  nn:=nn+1;
                                  twG[nn]:=round(tw-273);
                                  twnG[nn]:=twNp-273;
                                  tmnG[nn]:=t[1,2]-273;
                                  tmvG[nn]:=t[n,2]-273;
                                  tmcG[nn]:=t[round(n/2),2]-273;
                                end;
       time:=time+dtime;
     end;
     nnSv2:=nn;
     QmSv2:=Qm_ud2*G-QmMet-QmSv1;
     for i:=1 to n do
         tx[i,3]:=t[i,1];
           {НАГРЕВ МЕТАЛЛА В ТОМИЛЬНОЙ ЗОНЕ}
    w:=1.8;
    StCh;
    tw:=twTom;
{    twNp:=twNpk;}
    Fettling;
    Sio;
    QsioTom:=Ql*LsioTom;
    Qftom:=Qf*Ftom;
    twNp:=twNp2k;
   while time<time_H do
     begin
       Temp1;
       {twNp:=twNp2n+k4*((time_H/Nsteps*trunc(time*Nsteps/time_H))-timeMet-timeSv1);}
       Temp3;
            if time=ss*round(time/ss) then
                                begin
                                  nn:=nn+1;
                                  twG[nn]:=round(tw-273);
                                  twnG[nn]:=twNp-273;
                                  tmnG[nn]:=t[1,2]-273;
                                  tmvG[nn]:=t[n,2]-273;
                                  tmcG[nn]:=t[round(n/2),2]-273;
                                end;

       time:=time+dtime;
     end;
     QmTom:=Qm_ud2*G-QmMet-QmSv1-QmSv2;
     QmNp2:=Qm_ud1*G-QmNp1;
     tcpm:=0;
     for i:=1 to n do
        begin
         tx[i,4]:=t[i,1];
         tcpm:=tcpm+tx[i,4]/n;
        end;
{    if tx[n,4]>tmk then  time_H2:=time_H
                   else  time_H1:=time_H;
    if abs(tx[n,4]-tmk)>5 then goto label2;}
    {G:=Lp*b*s*2*ro((900))/time_H/1000*3600;  }
     ccp:=ccp/(n-1)/(time_H/dtime);
         {РАСЧЁТ ТЕПЛОВОГО БАЛАНСА}
   Qd_Tom_ud:=v*Cd(twTom)*(twTom-273);
   Qd_Sv2_ud:=v*Cd(twSv2)*(twSv2-273);
   Qd_Sv1_ud:=v*Cd(twSv1n)*(twSv1n-273);
   Qd_Np2_ud:=v*Cd(twNp2n)*(twNp2n-273);

   QwindowTom:=2.89*6.7*sqr(sqr(twTom/100));
   QwindowMet:=3.34*6.7*sqr(sqr(twMetn/100));

   B_Tom:=(QmTom+QfTom{+QsioTom{}+QwindowTom)/(Q+Qft+Qfv-Qd_Tom_ud);
   Qtr_Sv2:=B_Tom*v*((twTom-273)*cd(twTom)-(twSv2-273)*cd(twSv2));
   B_Sv2:=(QmSv2+QfSv2{+QsioSv2{}-Qtr_Sv2)/
                               (Q+Qft+Qfv-Qd_Sv2_ud);
   Qtr_Sv1:=(B_Tom+B_Sv2)*v*((twSv2-273)*cd(twSv2)-(twSv1n-273)*
          cd(twSv1n));
   B_Sv1:=(QmSv1+QfSv1+kSv1{!}*(QmNpSv1{}+QsioSv1{})-Qtr_Sv1)/(Q+Qft+Qfv-Qd_Sv1_ud);
   B_Np:=(QsioSv2+QsioTom+QmNp2)/(Q+Qft+Qfv-Qd_Np2_ud);

   B:=B_Tom+B_Sv1+B_Sv2+B_Np;

  { twMetNpk_:=twMetNpk;
   twMetNpk:=(((twNp2n-273)*cd(twNp2n)-(1-kSv1){!}{*(QmNpSv1+QsioSv1)/(B_Np)/v)/
           cd(twMetNpk)+273+twMetNpk)/2;
   if abs(twMetNpk-twMetNpk_)>1 then goto label2;     }

{   twMetn_:=twMetn;    }
   {twMetn:=(((twSv1n-273)*cd(twSv1n)+(twMetNpk-273)*cd(twMetNpk)-
                                  (QmMet+QfMet+(QmNpMet+QsioMet))/
           (B_Tom+B_Sv1+B_Sv2+B_Np)/v)/
           cd(twMetn)+273+twMetn)/2;      }
{twMetn:=(B_Np*cd(twMetNpk)*(twMetNpk-273)+(B_Sv1+B_Sv2+B_Tom)*cd(twSv1n)*(twSv1n-273)-
             (QmMet+QfMet+QmNpMet+QsioMet+QwindowMet)/v)/
             (B*cd(twMetn){*v}{)+273;
    writeln((twMetn-273):5:0);

   if abs(twMetn-twMetn_)>1 then goto label2; }

{   twNpn_:=twNp1n;
   twNp1n:=(((twNp2n-273)*cd(twNp2n)-((QmNpMet+QsioMet)+0.6*(QmNpSv1+QsioSv1{))/(B_Np)/v)/
           cd(twNp1n)+273+twNp1n)/2;
   if abs(twNp1n-twNpn_)>10 then goto label1;    }

   Qtr_Met:=(B_Tom+B_Sv1+B_Sv2)*v*((twSv1n-273)*cd(twSv1n)-(twMetn_-273)*cd(twMetn_))
             {    -B_Np*v*((twMetNpk-273)*cd(twMetNpk)-(twMetn_-273)*cd(twMetn_))} ;
 {  Qtr_Np1:=B_Np*v*((twNp2n-273)*cd(twNp2n)-(twNp1n-273)*cd(twNp1n));}

   Qd_Tom:=Qd_Tom_ud*B_Tom;
   Qd_Sv2:=Qd_Sv2_ud*B_Sv2;
   Qd_Sv1:=Qd_Sv1_ud*B_Sv1;
   Qd_Np2:=Qd_Np2_ud*B_Np;

     B_ud:=B/G*1000;
     labelb:
   ClrScr;
   writeln('               РАСЧЕТ НАГРЕВА МЕТАЛЛА');
                                                textcolor(6);
   writeln('   МЕТОДИЧЕСКАЯ ЗОНА');             textcolor(2);
   writeln('tпечи=(',(twMetn-273):3:0,'-',(twSv1n-273):3:0,
   ')^C     tпов1=',(tx[n,1]-273):5:0,'^C     tпов2=',(tx[1,1]-273):5:0,'^C  Tц=',(Tx[round(n/2),1]-273):0:0,'^C');
   writeln('tниз =(',(twMetn-273-50):3:0,'-',(twMetNpk-273):4:0,')^C');
                                                textcolor(6);
   writeln('   ПЕРВАЯ СВАРОЧНАЯ ЗОНА');         textcolor(2);
   writeln('tпечи=(',(twSv1n-273):4:0,'-',(twSv2-273):4:0,')^C    tпов1=',
       (tx[n,2]-273):5:0,'^C     tпов2=',(tx[1,2]-273):5:0,'^C  Tц=',(Tx[round(n/2),2]-273):0:0,'^C');
   writeln('tниз =(',(twMetNpk-273):3:0,'-',(twNp2n-273):4:0,')^C');
                                                textcolor(6);
   writeln('   ВТОРАЯ СВАРОЧНАЯ ЗОНА');         textcolor(2);
   writeln('tпечи=      ',(twSv2-273):5:0,'^C    tпов1=',
       (tx[n,3]-273):5:0,'^C     tпов2=',(tx[1,3]-273):5:0,'^C  Tц=',(Tx[round(n/2),3]-273):0:0,'^C');
   writeln('tниз =       ',(twNp2n-273):4:0,'^C');
                                                textcolor(6);
   writeln('   ТОМИЛЬНАЯ ЗОНА');                textcolor(2);
   writeln('tпечи=      ',(twTom-273):5:0,'^C    tпов1=',(tx[n,4]-273):5:0,
       '^C     tпов2=',(tx[1,4]-273):5:0,'^C  Tц=',(Tx[round(n/2),4]-273):0:0,'^C');
   writeln('tниз =       ',(twNp2k-273):4:0,'^C');
  writeln;
  writeln('Время нагрева                         ',trunc(time_H/3600),' ч ',
                  ((time_H/3600-trunc(time_H/3600))*60):2:0,' мин') ;
  writeln('Масса сляба                           ',(Mslab/1000):2:3,' т');
  writeln('Производительность печи               ',(G/1000*3600):2:2,' т/час');
  writeln('Среднемассовая температура металла    ',(Tcpm-273):4:0,'^C');
  writeln('Конечный перепад температур           ',(t[n,1]-t[trunc(n/2),1]):0:1,' ^C');
  writeln('Максимальный перепад температур       ',dtmax:0:0,' ^C');
  writeln('Кол-во теплоты получаемое металлом    ',(Qm_ud/1000):0:0,' кДж/кг');
{  writeln('Кол-во теплоты получаемое металлом_   ',((QmMet+QmSv1+QmSv2+QmTom+QmNp1+QmNp2)/G/1000):0:0,' кДж/кг');
{  writeln('Мощность нагрева металла              ',(Qm_ud/1000*G):0:0,' кВт');
  writeln('Средняя теплоёмкость металла        ',Ccp:5:0,' Дж/(кг*K)');         }
  readln;
  ClrScr;
   if dtmax>dtdop then writeln('НЕДОПУСТИМЫЙ ПЕРЕПАД ТЕМПЕРАТУР');
  writeln('Расход топлива на печь                ',(B/1000*3600):0:2,'тыс. м^3/час     ');
{  writeln('                                      ',(B*3600):0:0,' м^3/час');}
   writeln('Расход топлива по зонам:');
   writeln('        -в первой сварочной зоне      ',(B_Sv1/1000*3600):0:3,'тыс. м^3/час   ',(B_Sv1/B*100):0:1,' %');
   writeln('        -во второй сварочной зоне     ',(B_Sv2/1000*3600):0:3,'тыс. м^3/час   ',(B_Sv2/B*100):0:1,' %');
   writeln('        -в томильной зоне             ',(B_Tom/1000*3600):0:3,'тыс. м^3/час   ',(B_Tom/B*100):0:1,' %');
   writeln('        -в зоне нижнего подогрева     ',(B_Np/1000*3600):0:3,'тыс. м^3/час   ',(B_Np/B*100):0:1,' %');
  writeln('Удельный расход топлива               ',B_ud:0:0,' м^3/т   ');
  writeln('Удельный расход природного газа       ',(B_ud*x_):0:0,' м^3/т');
{  writeln('                                      ',(B_ud*Q/1000000):0:0,' МДж/т');}
  writeln('                                      ',(B_ud*Q/1000000/29.33):0:1,' кг у.т./т');
  writeln('Себестоимость нагрева                 ',(B_ud*Ts/1000):0:2,' грн/т');
        Qpr:=B*(Q+Qfv+Qft);
        Qm:=Qm_ud*G;
        Qm_:=Qm/Qpr*100;
   writeln('КПД нагрева                          ',Qm_:5:1,' %');
   readln;

   Balance;

grD:=Detect;
InitGraph(grD,grM,'c:\egavga.bgi');
Err:=GraphResult;
if Err=grOk then
 begin
 GraPhics;
  closegraph;
   { if ord(readkey)=13 then goto labelb;  }
 end;
{Close(ww);  }
END.