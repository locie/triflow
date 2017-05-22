Search.setIndex({docnames:["cookbook","cookbook/advection_diffusion","cookbook/burger_equation","cookbook/burger_kdv_equation","cookbook/so_wavy","cookbook/wave_equation","index","installation","modules","overview","schemes","triflow","triflow.core","triflow.plugins"],envversion:53,filenames:["cookbook.rst","cookbook/advection_diffusion.rst","cookbook/burger_equation.rst","cookbook/burger_kdv_equation.rst","cookbook/so_wavy.rst","cookbook/wave_equation.rst","index.rst","installation.rst","modules.rst","overview.rst","schemes.rst","triflow.rst","triflow.core.rst","triflow.plugins.rst"],objects:{"":{triflow:[11,0,0,"-"]},"triflow.core":{fields:[12,0,0,"-"],model:[12,0,0,"-"],routines:[12,0,0,"-"],simulation:[12,0,0,"-"]},"triflow.core.fields":{BaseFields:[12,1,1,""]},"triflow.core.fields.BaseFields":{array:[12,2,1,""],copy:[12,3,1,""],dependent_variables:[12,2,1,""],factory:[12,4,1,""],fill:[12,3,1,""],flat:[12,2,1,""],helper_functions:[12,2,1,""],size:[12,2,1,""],structured:[12,2,1,""],uarray:[12,2,1,""],uflat:[12,2,1,""]},"triflow.core.model":{Model:[12,1,1,""],load_model:[12,5,1,""]},"triflow.core.model.Model":{F:[12,2,1,""],F_array:[12,2,1,""],J:[12,2,1,""],J_array:[12,2,1,""],Properties:[12,2,1,""],fields_template:[12,2,1,""],sargs:[12,2,1,""],save:[12,3,1,""]},"triflow.core.routines":{F_Routine:[12,1,1,""],J_Routine:[12,1,1,""],ModelRoutine:[12,1,1,""]},"triflow.core.routines.F_Routine":{diff_approx:[12,3,1,""]},"triflow.core.simulation":{Simulation:[12,1,1,""]},"triflow.core.simulation.Simulation":{compute:[12,3,1,""],dt:[12,2,1,""],fields:[12,2,1,""],i:[12,2,1,""],id:[12,2,1,""],model:[12,2,1,""],physical_parameters:[12,2,1,""],status:[12,2,1,""],t:[12,2,1,""],tmax:[12,2,1,""]},"triflow.plugins":{displays:[13,0,0,"-"],schemes:[13,0,0,"-"],signals:[13,0,0,"-"]},"triflow.plugins.displays":{amnesic_mean:[13,5,1,""],bokeh_fields_update:[13,5,1,""],bokeh_probes_update:[13,5,1,""],coroutine:[13,5,1,""],visdom_update:[13,5,1,""],window_data:[13,5,1,""]},"triflow.plugins.schemes":{RODASPR:[13,1,1,""],ROS2:[13,1,1,""],ROS3PRL:[13,1,1,""],ROS3PRw:[13,1,1,""],ROW_general:[13,1,1,""],Theta:[13,1,1,""],scipy_ode:[13,1,1,""]},"triflow.plugins.schemes.ROW_general":{__call__:[13,3,1,""]},"triflow.plugins.schemes.Theta":{__call__:[13,3,1,""]},"triflow.plugins.schemes.scipy_ode":{__call__:[13,3,1,""]},"triflow.plugins.signals":{AdditiveSignal:[13,1,1,""],ConstantSignal:[13,1,1,""],GaussianBrownNoise:[13,1,1,""],GaussianWhiteNoise:[13,1,1,""],Signal:[13,1,1,""],SinusoidalSignal:[13,1,1,""]},"triflow.plugins.signals.Signal":{__add__:[13,3,1,""],__call__:[13,3,1,""],__sub__:[13,3,1,""],fourrier_spectrum:[13,2,1,""]},triflow:{core:[12,0,0,"-"],plugins:[13,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","attribute","Python attribute"],"3":["py","method","Python method"],"4":["py","staticmethod","Python static method"],"5":["py","function","Python function"]},objtypes:{"0":"py:module","1":"py:class","2":"py:attribute","3":"py:method","4":"py:staticmethod","5":"py:function"},terms:{"1go":9,"4th":13,"6th":[12,13],"break":9,"case":9,"class":[6,10,12,13],"default":[1,2,3,4,5,12,13],"final":[1,2,4],"float":[12,13],"function":[4,5,9,10,12,13],"import":[1,2,3,4,5,9,12,13],"int":[12,13],"long":9,"new":[9,10],"return":[1,2,3,4,5,9,10,12,13],"static":12,"transient":9,"true":[1,2,3,4,5,9,12,13],"try":13,"var":13,For:9,IDE:7,Its:12,Not:12,The:[0,4,5,6,7,9,10,12,13],These:9,Useful:13,Will:[12,13],With:10,__add__:13,__call__:[10,12,13],__init__:10,__sub__:13,abil:10,abl:[9,12,13],accept:9,access:[9,10,12,13],account:10,accuraci:13,acoust:2,across:9,actual:[9,10,12,13],adapt:13,added:13,addhandl:13,addit:13,additivesign:13,addr:13,adress:13,advantag:9,advect:[1,9],after:[9,13],aggress:9,agreement:13,aim:9,algebra:12,algorithm:[9,10],alias:13,aliased_sign:13,all:[0,9,10,12,13],allow:[9,10,12,13],alpha:[1,2,3,4,5,13],amnesic_mean:13,amplitud:13,anaconda:[],anaconda_:7,ani:[10,12,13],appli:2,approxim:[9,12],area:2,arg:[12,13],argmax:13,argument:[6,10,12,13],around:[10,12,13],arrai:[9,12],ask:[1,2,3,4,5],atol:13,attempt:3,attribut:[9,10,12],automat:[1,2,3,4,5,9],autonom:12,avail:[0,6,9,13],avoid:9,awar:9,b_pred:13,backward:[9,10,13],backwardeul:10,bad:10,base:[7,12,13],basefield:12,basic:9,bdc:10,becaus:9,been:9,befor:[9,10,13],behaviour:2,being:9,best:9,better:9,between:[9,13],bewar:10,binari:[9,12],bokeh:[5,13],bokeh_fields_upd:13,bokeh_probes_upd:13,bokeh_upt:13,bool:[12,13],both:12,boundari:[5,6,10,12,13],brown:13,brown_sign:13,brownnois:13,build:12,built:9,burger:[0,6,9],cach:12,call:[9,10,12,13],callabl:[9,10,12,13],can:[7,9,10,12,13],careful:12,check:13,chemic:1,choic:[9,10],chosen:13,classic:9,close:13,cmap:3,code:9,coeffici:[10,13],color:[1,2,3,4,5],colorbar:3,column:9,com:7,combin:1,combinaison:10,compil:[6,7,12],complex:9,compress:9,comput:[9,12,13],concaten:13,concentr:1,condit:[1,2,3,4,5,6,10,12,13],conditionn:[12,13],configur:9,constant:[1,9],constantsign:13,contain:[6,10,12,13],content:[6,8],control:[6,13],convect:[0,2,6,12],convert:9,cookbook:6,coordin:9,copi:[9,10,12],core:[6,8,11],coroutin:[9,13],correspond:9,cos:[4,9,12,13],cosh:3,cosin:4,cost:9,could:1,count:9,coupl:[0,6,12],cpu:9,crank:[9,10,13],creat:12,csc:[10,12],custom:13,cut:13,dae:10,darkr:[1,2,3,4,5],data:[3,9,12,13],deal:9,debug:9,decomposit:9,dedalu:3,deeplearn:7,def:[5,9,10,13],defin:9,dens:12,densiti:13,dep_var:9,depend:[9,10,12,13],dependeci:7,dependent_vari:[9,12],deriv:[9,12],describ:1,descript:13,design:9,detail:9,dict:[1,2,3,4,5,9,12,13],dictionnari:[12,13],diff_approx:12,differ:[9,10,12,13],differenti:[2,5,10,12],differential_equ:[9,12],diffus:[0,2,6,9,12],digibib:[10,13],dimens:9,directli:13,dirichlet:[5,9],dirichlet_condit:9,disadvantag:9,discontinu:2,discret:[1,2,3,4,5],discretis:[9,12],disk:9,displai:[1,2,3,4,5,6,8,11],distribut:7,docid:[10,13],document:9,domain:[1,2,3,4,5],dt_min:13,due:1,dure:[9,13],dxu:[1,2,3,4,9,12],dxv:[4,12],dxxu:[1,2,3,4,5,9,12,13],dxxv:[4,12],dxxxu:3,dynam:[2,9,12],each:[5,9],easi:9,easili:9,edg:[5,9],effici:[9,12],element:9,emploi:9,end:[1,2,3,4,5,9],endpoint:[1,2,3,4,12,13],energi:1,ensur:13,enumer:[1,2,3,4,5,9],env:13,environn:13,eps:12,eq_diff:9,equat:[0,6,9,10,12,13],error:13,especiali:9,euler:[9,10,13],evalu:[9,13],everi:[9,12,13],exampl:[1,9,12,13],exclud:[1,2,4],exempl:9,expect:2,expos:12,expr:12,express:[9,12],extens:9,extern:6,extra:[7,9,10,12,13],f_arrai:12,f_routin:12,factor:13,factori:[9,12],fail:12,fals:[1,2,3,4,5,9,12,13],far:9,fast:9,feed:[12,13],field:[1,2,3,4,5,6,8,10,11,13],fields_templ:[1,2,3,4,5,9,12,13],fig:13,fig_kwarg:13,figsiz:[1,2,3,4,5],figur:[1,2,3,4,5],file:12,filenam:12,fill:[10,12,13],fill_between:[1,2,3,4,5],filter:13,filter_std:13,filter_window_s:13,finish:12,finit:[9,12],first:[1,2,4,5,9,12],fit:9,fix:[5,9,10],flag:[1,2,4,5,7],flat:12,flat_arrai:12,flatten:[10,12],float64:9,flow:2,fluid:[1,2],fly:[9,10],folder:9,follow:[9,10,12,13],footprint:9,forc:13,forcedsign:13,form:[9,12],format:[9,10],fortran:[7,9],forward:[2,9,10,13],found:13,fourrier:13,fourrier_spectrum:13,fraction:13,frequenc:13,frequency_cut:13,frequency_sampl:13,from:[1,2,3,4,5,9,12,13],full:[7,9,10],full_data:3,func:13,functool:[1,2,3,4,5],fundament:2,further:9,gamma:13,gas:2,gaussian:[1,2,3,4,5,13],gaussianbrownnois:13,gaussianwhitenois:13,gener:[9,12,13],getlogg:13,git:7,github:6,give:[9,10,12,13],goe:13,good:[10,13],gpu:9,granular:9,graph:9,grow:[2,9],hand:12,handi:9,handl:9,handler:13,has:[9,10,13],have:[5,9,10,12,13],help_funct:[9,12],helper:[9,12],helper_funct:12,herlper:12,high:[9,12],higher:[6,10],highest:13,hire:9,hook:[5,6,10,12,13],host:9,how:10,howev:10,html:[3,7],http:[7,10,13],ident:10,imag:3,implement:[9,13],implicit:12,improv:10,includ:[7,9,12,13],independ:9,index:6,info:13,inform:7,informationto:13,init:13,initi:[1,2,3,4,5,9,10,12,13],inject:9,inlin:[1,2,3,4,5],inplac:12,input:[10,12],ins:9,insid:[1,9],instal:6,instanti:9,integr:[9,10,12,13],integrator_kwarg:13,interact:[9,13],intern:[6,9,12,13],interpol:13,involv:9,ipython:3,isclos:13,iter:[1,2,3,4,5,9,12,13],itertool:9,its:[9,10],j_arrai:12,j_routin:12,jacobian:[9,10,12],joachim:10,johann:2,jupyt:[7,9,13],just:[9,13],kdv:[0,6],keep:13,kei:[12,13],kept:13,keyerror:12,keyword:[10,13],known:9,kwarg:[12,13],kwd_integr:10,label:9,lambda:[10,12,13],larg:[9,10],last:[7,9,13],later:9,launch:13,lead:[2,5,9,10,13],leav:13,legend:9,lenght:13,less:9,level:[6,12],librari:[7,9],lightsteelblu:4,like:[0,6,7,9],linalg:13,line:13,line_kwarg:13,linear:[12,13],link:9,linspac:[1,2,3,4,5,9,12,13],list:[6,9,12,13],live:9,ljust:[1,2,3,4,5],load:12,load_model:[9,12],loc:9,loci:7,log:[1,2,3,4,5,13],logger:13,loop:9,low:13,main:[7,9,12,13],make:[9,10],mandatori:9,manipul:12,martinu:2,mathemat:[2,9,12],matplotlib:[1,2,3,4,5],matrix:[9,12,13],max:[1,2,3,4,5,13],max_it:13,maximum:13,mean:[9,13],mean_coroutin:13,mean_prob:13,mechan:2,memori:[9,10,13],mendatori:12,merg:[1,2,4],method:[9,10,12,13],min:[1,2,3,4,5],minimum:13,miss:12,mix:9,mode:[9,13],model:[1,2,3,4,5,6,8,10,11,13],modelroutin:12,modif:[9,10,12],modifi:[9,12,13],modul:[6,8,9],modular:9,more:9,moreov:9,motiv:6,move:2,multiprocess:[1,2,3,4,5,9],name:[2,9,12,13],nbviewer:0,ndarrai:[12,13],need:[7,12],net:7,network:9,new_field:9,new_t:9,next:[12,13],nicolson:[9,10,13],node:[1,2,4,9,12],nois:13,noise_with_offset:13,noise_without_offset:13,noisi:13,non:12,none:[12,13],nonlinear:2,normal:13,notat:12,notebook:[0,3,9,13],notic:9,notimplementederror:13,number:[9,10,12,13],numer:6,numpi:[1,2,3,4,5,9,12,13],nxn:9,object:[9,10,12,13],obtain:[9,13],occur:2,ode:[9,10,12,13],odes:10,offset:13,old:7,one:[9,10,12,13],onli:[9,10,12,13],optim:[9,12],option:[6,12,13],optionn:[9,13],order:[5,9,10,12,13],orient:7,other:[1,9],other_sign:13,our:[1,2,3,4,5],output:[9,10,12],output_notebook:13,outsid:9,overhead:9,overview:6,own:10,packag:[6,7,8],pad:9,page:[6,7],par:[5,9,10,12,13],param:13,paramet:[1,2,3,4,5,6,10,12,13],parent:10,pars:9,part:[9,13],partial:[2,12],particl:1,pass:[10,12,13],path:12,pcolormesh:3,pde:9,pdf:9,perform:[9,10,12,13],period:[1,2,3,4,5,9,12,13],periodogram:13,phase:13,phenomena:1,physic:[1,12,13],physical_paramet:12,pickabl:9,pickl:12,pip:7,plot:[1,2,3,4,5,9,13],plug:9,plugin:[6,8,9,11,12],png:[3,9],posit:12,possibl:[9,10],post:[9,13],potenti:9,power:13,pre:12,precis:[1,2,3,4,5],predictor:13,present:10,previou:[9,12],print:[1,2,3,4,5,9,12,13],privileg:7,probe:13,process:[1,9,13],project:[3,7],properli:9,properti:[9,12],provid:[1,2,3,4,5,9,10,12,13],proxi:[9,13],pseudo:13,puls:[1,2,5],purpos:9,put:12,pylab:[1,2,3,4,5,9],pypi:6,python:7,quantiti:1,rais:[12,13],randn:13,random:13,rang:10,reach:12,read:[1,2,9],real:5,rec:12,recommend:7,redond:[1,2,4],reduc:[9,12],reflect:12,regroup:13,rel:13,reload:9,repeat:9,repositori:7,repres:10,reproduc:3,reproduct:13,request:13,requir:6,resolut:9,result:3,retstep:[1,2,3,4,5,9],right:12,rodaspr:[9,10,12,13],roll:[1,5],root:7,rope:5,ros2:[10,13],ros3prl:[10,13],ros3prw:[10,13],rosenbrock:[10,13],routin:[8,9,10,11],row:[9,12],row_gener:[6,13],run:12,runtimeerror:13,sae:9,same:[3,9,10,12,13],sampl:13,sarg:12,save:[9,12,13],saved_data:13,scalabl:9,scalar:[9,12],scheme:[1,2,3,4,5,6,8,11,12],scientif:7,scipi:[1,2,3,4,5,9,10,12,13],scipy_od:[6,13],scpy:13,seaborn:[1,2,3,9],search:6,second:[9,13],section:[9,10],see:[7,9],seed:13,self:10,send:[3,13],sent:9,server:13,set:[1,2,4,5,12,13],setlevel:13,shock:2,should:[9,12],show:[1,2,3,4,5,9],side:12,signal1:13,signal2:13,signal3:13,signal:[1,2,3,4,5,8,11],signal_a:13,signal_b:13,signal_period:13,signam:13,signatur:[10,12,13],similar:13,simpl:[2,9,12,13],simplifi:9,simul:[1,2,3,4,5,6,8,11,13],sin:[4,5,12],sine:4,sinusoid:13,sinusoidalsign:13,size:[1,2,5,10,12,13],slow:12,slug:12,smooth:2,snippet:9,softwar:7,solut:[9,13],solv:[3,9,10,12,13],solver:[6,10,12,13],some:[9,13],somm:9,sourc:[9,12,13],space:[10,12],spars:[9,10,12,13],sparsiti:9,spatial:[1,2,3,4,5,9,12],speci:1,special:[9,12],specif:[12,13],spectrum:13,spectrum_dens:13,spectrum_frequ:13,sps:10,spsolv:13,stai:13,state:[12,13],statu:12,std:13,step:[1,2,3,4,5,9,10,12,13],stiff:10,stop:12,store:[9,12],str:[12,13],strategi:9,streamhandl:13,structur:[6,12],style:[1,2,3,9],subarrai:9,submodul:[8,11],subpackag:[6,8],sudo:7,suitabl:10,sum:13,superlu:9,suppos:13,sure:10,symbol:[9,12],sympi:[9,12],system:[1,4,5,9,10,12,13],take:[9,10,12,13],taken:10,target:9,temperatur:1,templat:13,tempor:[6,12,13],term:2,than:9,theano:[7,9,12],thei:[9,10,13],them:9,theta:[6,9,13],thi:[2,3,5,7,9,10,12,13],third:13,three:[1,5],thu:[7,9],time:[5,9,10,12,13],time_step:[1,2,3,4,5,13],tmax:[1,2,3,4,5,9,12,13],tol:[2,3,4,13],toler:13,too:13,took:13,tool:9,tradit:10,traffic:2,transfer:1,transform:12,triflow:[1,2,3,4,5,7,9],tupl:[12,13],tutori:3,two:[1,9],type:[9,12,13],typic:10,u_m1:9,u_p1:9,uarrai:12,uflat:[10,12],ufunc:12,under:13,unknown:9,until:[1,2,3,4,5,12],updat:[7,10,12,13],upgrad:7,usag:[9,10],use:[1,2,3,7,9,10,12],used:[9,10,12,13],useful:13,user:[7,9,13],using:[7,13],valid:10,valu:[9,10,13],valueerror:13,vanilla:12,variabl:[9,10,12,13],variou:2,vector:9,veloc:[1,2,5],veri:9,version:7,via:[0,6,9],view:[9,12],viridi:3,viscou:2,visdom:13,visdom_upd:13,visdom_upt:13,vode:13,wai:[9,12],wanner:[10,13],want:[1,2,4,5,7,10,13],warn:13,wave:[0,2,6,13],weight:13,well:9,what:9,where:[1,12,13],whether:12,which:[1,2,4,5,9,10,12,13],white:[1,2,3,4,5,13],whitegrid:9,whitenois:13,wikipedia:[1,2],window:13,window_data:[3,13],window_len:13,window_save_gen:13,without:[7,13],word:12,work:9,wrap:9,wrapper:10,write:[6,10],written:[5,7,9,10,12,13],www:[10,13],x_mean:13,xlim:[1,2,3,4,5,9],yield:12,you:[7,9,13],your:10,zeros_lik:5,zorder:[1,2,3,4,5]},titles:["Cookbook","The convection diffusion equation","The burger equation","The burger - kdv equation","Coupled burger\u2019s-like equations","Wave equation","Welcome to triflow\u2019s documentation!","Installation","triflow","Overview","Temporal schemes","triflow package","triflow.core package","triflow.plugins package"],titleterms:{"class":9,The:[1,2,3],argument:9,avail:10,boundari:9,burger:[2,3,4],compil:9,condit:9,contain:9,content:[11,12,13],control:9,convect:1,cookbook:0,core:12,coupl:4,diffus:1,displai:[9,13],document:6,equat:[1,2,3,4,5],extern:7,field:[9,12],github:7,higher:9,hook:9,indic:6,instal:7,intern:10,kdv:3,level:9,like:4,list:10,model:[9,12],modul:[11,12,13],motiv:9,numer:9,option:9,overview:9,packag:[11,12,13],paramet:9,plugin:13,pypi:7,requir:7,routin:12,row_gener:10,scheme:[9,10,13],scipy_od:10,signal:13,simul:[9,12],solver:9,structur:10,submodul:[12,13],subpackag:11,tabl:6,tempor:[9,10],theta:10,triflow:[6,8,11,12,13],via:7,wave:5,welcom:6,write:9}})