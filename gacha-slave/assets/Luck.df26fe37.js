var D=Object.defineProperty;var h=Object.getOwnPropertySymbols;var g=Object.prototype.hasOwnProperty,B=Object.prototype.propertyIsEnumerable;var F=(n,l,e)=>l in n?D(n,l,{enumerable:!0,configurable:!0,writable:!0,value:e}):n[l]=e,v=(n,l)=>{for(var e in l||(l={}))g.call(l,e)&&F(n,e,l[e]);if(h)for(var e of h(l))B.call(l,e)&&F(n,e,l[e]);return n};import{d as E,r as i,C as V,D as k,I as A,J as T,K as W,o as x,q as I,f as s,w as d,e as N,L as U,F as $,s as O,h as b}from"./vendor.7622e4b8.js";import{U as P}from"./index.esm.min.c6bc6a12.js";import{a as R}from"./wish.bbfca896.js";const S=b("\u8BA1\u7B97"),q=b("\u91CD\u7F6E"),M=E({setup(n){const l={nTotalWishes:999,nGolds:16},e=i(v({},l)),y=()=>{e.value=v({},l)},p=i(0),C=i(0),a=i({tooltip:{trigger:"axis"},toolbox:{show:!0,feature:{mark:{show:!0},dataView:{show:!0,readOnly:!1},restore:{show:!0},saveAsImage:{show:!0}}},legend:{data:["n\u91D1\u6982\u7387","\u2264n\u91D1\u6982\u7387"],left:0},xAxis:[{type:"category",data:[1,2],axisPointer:{type:"shadow"}}],yAxis:[{type:"value"}],grid:{bottom:"50%"},series:[{name:"n\u91D1\u6982\u7387",type:"bar",tooltip:{valueFormatter:t=>t>.001?`${(t*100).toFixed(1)}%`:t},data:[.1,.8]},{name:"\u2264n\u91D1\u6982\u7387",type:"line",tooltip:{valueFormatter:t=>t<.999?`${(t*100).toFixed(1)}%`:t},data:[.1,.9]},{name:"\u6B27\u975E\u8BC4\u4EF7",type:"pie",itemStyle:{borderRadius:10,borderColor:"#fff",borderWidth:2},radius:"32%",center:["50%","78%"],z:100,label:{formatter:"{b} ({d}%)",overflow:"breakAll"},data:[{name:"\u91D1\u6570\u66F4\u5C11",value:0},{name:"\u91D1\u6570\u76F8\u540C",value:0},{name:"\u91D1\u6570\u66F4\u591A",value:1}]}]}),c=i(!1),G=()=>{e.value.nGolds=Math.min(e.value.nGolds,e.value.nTotalWishes),a.value.xAxis[0].data=[],a.value.series[0].data=[],a.value.series[1].data=[],a.value.series[2].data[0].value=0,a.value.series[2].data[1].value=0,a.value.series[2].data[2].value=1;let t=R("weapon_5",e.value.nTotalWishes,0,"00",(o,u)=>o>=.999&&u>=e.value.nGolds),r=0;for(let o=0;o<t.length;++o){let u=t[o];r+=u,u>0&&(a.value.xAxis[0].data.push(o),a.value.series[1].data.push(r),o==e.value.nGolds?a.value.series[0].data.push({value:u,itemStyle:{color:"orange"}}):a.value.series[0].data.push(u)),o==e.value.nGolds&&(a.value.series[2].data[0].value=r-u,a.value.series[2].data[1].value=u,a.value.series[2].data[2].value=1-r)}t.length-1<e.value.nGolds&&(a.value.series[2].data[0].value=1,a.value.series[2].data[1].value=0,a.value.series[2].data[2].value=0),p.value=e.value.nTotalWishes,C.value=e.value.nGolds,c.value=!0};return(t,r)=>{const o=V,u=k,f=A,w=T,_=W;return x(),I($,null,[s(_,{header:"\u53C2\u6570"},{default:d(()=>[s(w,{ref:"ruleFormRef",model:e.value,"status-icon":"","label-width":"auto",class:"demo-ruleForm"},{default:d(()=>[s(u,{label:"\u603B\u62BD\u6570",prop:"nTotalWishes"},{default:d(()=>[s(o,{modelValue:e.value.nTotalWishes,"onUpdate:modelValue":r[0]||(r[0]=m=>e.value.nTotalWishes=m),min:1},null,8,["modelValue"])]),_:1}),s(u,{label:"\u4E94\u661F\u6570",prop:"nGolds"},{default:d(()=>[s(o,{modelValue:e.value.nGolds,"onUpdate:modelValue":r[1]||(r[1]=m=>e.value.nGolds=m),min:0},null,8,["modelValue"])]),_:1}),s(u,null,{default:d(()=>[s(f,{type:"primary",onClick:G},{default:d(()=>[S]),_:1}),s(f,{onClick:y},{default:d(()=>[q]),_:1})]),_:1})]),_:1},8,["model"])]),_:1}),c.value?(x(),N(_,{key:0,header:`${p.value}\u62BD\u65F6\u91D1\u6570\u7684\u5206\u5E03`},{default:d(()=>[s(O(P),{style:{height:"500px"},option:a.value},null,8,["option"])]),_:1},8,["header"])):U("",!0)],64)}}});export{M as default};
