var X=(f,p,c)=>new Promise((a,t)=>{var r=m=>{try{y(c.next(m))}catch(x){t(x)}},u=m=>{try{y(c.throw(m))}catch(x){t(x)}},y=m=>m.done?a(m.value):Promise.resolve(m.value).then(r,u);y((c=c.apply(f,p)).next())});import{c as A,r as Y,a as T,b as me,d as pe,e as I,u as Z,f as fe,w as ee,n as ve,o as _,g as N,h,i as g,j as i,P as ge,k as U,l as j,m as D,p as l,q as G,s as k,t as L,C as _e,v as te,Q as ye,X as M,x as he,F as se,y as le,z,Y as be,A as ae,B as oe,J as xe,D as re,E as ke,_ as ne,G as we,H as Ce,I as Ve,K as $e,L as B,M as J,N as ie,O as ue,R as Le,S as Se,T as Pe,U as qe,V as Te,W as Ie}from"./vendor.ef741aee.js";const Ue=function(){const p=document.createElement("link").relList;if(p&&p.supports&&p.supports("modulepreload"))return;for(const t of document.querySelectorAll('link[rel="modulepreload"]'))a(t);new MutationObserver(t=>{for(const r of t)if(r.type==="childList")for(const u of r.addedNodes)u.tagName==="LINK"&&u.rel==="modulepreload"&&a(u)}).observe(document,{childList:!0,subtree:!0});function c(t){const r={};return t.integrity&&(r.integrity=t.integrity),t.referrerpolicy&&(r.referrerPolicy=t.referrerpolicy),t.crossorigin==="use-credentials"?r.credentials="include":t.crossorigin==="anonymous"?r.credentials="omit":r.credentials="same-origin",r}function a(t){if(t.ep)return;t.ep=!0;const r=c(t);fetch(t.href,r)}};Ue();const Re="modulepreload",ce={},je="/assets/happay/get-travel-request-docs/",de=function(p,c){return!c||c.length===0?p():Promise.all(c.map(a=>{if(a=`${je}${a}`,a in ce)return;ce[a]=!0;const t=a.endsWith(".css"),r=t?'[rel="stylesheet"]':"";if(document.querySelector(`link[href="${a}"]${r}`))return;const u=document.createElement("link");if(u.rel=t?"stylesheet":Re,t||(u.as="script",u.crossOrigin=""),u.href=a,document.head.appendChild(u),t)return new Promise((y,m)=>{u.addEventListener("load",y),u.addEventListener("error",m)})})).then(()=>p())},W=A({url:"frappe.auth.get_logged_user",cache:"User",onError(f){f&&f.exc_type==="AuthenticationError"&&O.push({name:"LoginPage"})}});function K(){let p=new URLSearchParams(document.cookie.split("; ").join("&")).get("user_id");return p==="Guest"&&(p=null),p}const E=Y({login:A({url:"login",makeParams({email:f,password:p}){return{usr:f,pwd:p}},onSuccess(f){W.reload(),E.user=K(),E.login.reset(),O.replace(f.default_route||"/")}}),logout:A({url:"logout",onSuccess(){W.reset(),E.user=K(),O.replace({name:"Login"})}}),user:K(),isLoggedIn:T(()=>!!E.user)}),De=[{path:"/",name:"Home",component:()=>de(()=>import("./Home.23906f4c.js"),["assets/Home.23906f4c.js","assets/vendor.ef741aee.js","assets/vendor.1875b906.css"])},{name:"Login",path:"/account/login",component:()=>de(()=>import("./Login.ae424f5c.js"),["assets/Login.ae424f5c.js","assets/vendor.ef741aee.js","assets/vendor.1875b906.css"])}];let O=me({history:pe("/get-travel-request-docs"),routes:De});O.beforeEach((f,p,c)=>X(void 0,null,function*(){let a=E.isLoggedIn;try{yield W.promise}catch(t){a=!1}f.name==="Login"&&a?c({name:"Home"}):f.name!=="Login"&&!a?c({name:"Login"}):c()}));const ze={class:"w-full"},Ee=["onClick"],Oe={class:"flex items-center"},Ae={key:0,class:"overflow-hidden text-ellipsis whitespace-nowrap text-base leading-5"},Ne={key:1,class:"text-base leading-5 text-gray-500"},Be={class:"mt-1 rounded-lg bg-white py-1 text-base shadow-2xl"},Fe={class:"relative px-1.5 pt-0.5"},He={key:0,class:"px-2.5 py-1.5 text-sm font-medium text-gray-500"},Ge={class:"flex flex-col space-y-1"},Me=["innerHTML"],Je={key:0,class:"mt-1.5 rounded-md px-2.5 py-1.5 text-base text-gray-600"},We={key:0,class:"border-t p-1.5 pb-0.5"},Ke={__name:"Autocomplete",props:{modelValue:{type:String,default:""},options:{type:Array,default:()=>[]},size:{type:String,default:"md"},variant:{type:String,default:"subtle"},placeholder:{type:String,default:""},disabled:{type:Boolean,default:!1},filterable:{type:Boolean,default:!0}},emits:["update:modelValue","update:query","change"],setup(f,{expose:p,emit:c}){const a=f,t=c,r=I(""),u=I(!1),y=I(null),m=Z(),x=fe(),d=T(()=>"value"in m),S=T({get(){return d.value?m.value:a.modelValue},set(s){r.value="",s&&(u.value=!1),t(d.value?"change":"update:modelValue",s)}});function n(){u.value=!1}const C=T(()=>{var e;return!a.options||a.options.length==0?[]:(((e=a.options[0])==null?void 0:e.group)?a.options:[{group:"",items:a.options}]).map((v,o)=>({key:o,group:v.group,hideLabel:v.hideLabel||!1,items:a.filterable?w(v.items):v.items})).filter(v=>v.items.length>0)});function w(s){return r.value?s.filter(e=>[e.label,e.value].some(o=>(o||"").toString().toLowerCase().includes(r.value.toLowerCase()))):s}function V(s){if(typeof s=="string"){let v=C.value.flatMap(o=>o.items).find(o=>o.value===s);return(v==null?void 0:v.label)||s}return s==null?void 0:s.label}ee(r,s=>{t("update:query",s)}),ee(u,s=>{s&&ve(()=>{y.value.el.focus()})});const P=T(()=>a.disabled?"text-gray-600":"text-gray-800"),F=T(()=>{let s={sm:"text-base rounded h-7",md:"text-base rounded h-8",lg:"text-lg rounded-md h-10",xl:"text-xl rounded-md h-10"}[a.size],e={sm:"py-1.5 px-2",md:"py-1.5 px-2.5",lg:"py-1.5 px-3",xl:"py-1.5 px-3"}[a.size],v=a.disabled?"disabled":a.variant,o={subtle:"border border-gray-100 bg-gray-100 placeholder-gray-500 hover:border-gray-200 hover:bg-gray-200 focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400",outline:"border border-gray-300 bg-white placeholder-gray-500 hover:border-gray-400 hover:shadow-sm focus:bg-white focus:border-gray-500 focus:shadow-sm focus:ring-0 focus-visible:ring-2 focus-visible:ring-gray-400",disabled:["border bg-gray-50 placeholder-gray-400",a.variant==="outline"?"border-gray-300":"border-transparent"]}[v];return[s,e,o,P.value,"transition-colors w-full"]});return p({query:r}),(s,e)=>(_(),N(i(xe),{modelValue:S.value,"onUpdate:modelValue":e[3]||(e[3]=v=>S.value=v),nullable:""},{default:h(({open:v})=>[g(i(ge),{class:"w-full",show:u.value,"onUpdate:show":e[2]||(e[2]=o=>u.value=o)},{target:h(({open:o,togglePopover:q})=>[U(s.$slots,"target",j(D({open:o,togglePopover:q})),()=>[l("div",ze,[l("button",{class:G(["flex w-full items-center justify-between focus:outline-none",F.value]),onClick:()=>q()},[l("div",Oe,[U(s.$slots,"prefix"),S.value?(_(),k("span",Ae,L(V(S.value)),1)):(_(),k("span",Ne,L(f.placeholder||""),1))]),g(i(_e),{class:"h-4 w-4 stroke-1.5"})],10,Ee)])])]),body:h(({isOpen:o})=>{var q;return[te(l("div",null,[l("div",Be,[l("div",Fe,[g(i(ye),{ref_key:"search",ref:y,class:"form-input w-full",type:"text",onChange:e[0]||(e[0]=b=>{r.value=b.target.value}),value:r.value,autocomplete:"off",placeholder:"Search"},null,8,["value"]),l("button",{class:"absolute right-1.5 inline-flex h-7 w-7 items-center justify-center",onClick:e[1]||(e[1]=b=>S.value=null)},[g(i(M),{class:"h-4 w-4 stroke-1.5"})])]),g(i(he),{class:"my-1 max-h-[12rem] overflow-y-auto px-1.5",static:""},{default:h(()=>[(_(!0),k(se,null,le(C.value,b=>te((_(),k("div",{class:"mt-1.5",key:b.key},[b.group&&!b.hideLabel?(_(),k("div",He,L(b.group),1)):z("",!0),(_(!0),k(se,null,le(b.items,$=>(_(),N(i(be),{as:"template",key:$.value,value:$},{default:h(({active:H,selected:Q})=>[l("li",{class:G(["flex items-center rounded px-2.5 py-2 text-base",{"bg-gray-100":H}])},[U(s.$slots,"item-prefix",ae({ref_for:!0},{active:H,selected:Q,option:$})),U(s.$slots,"item-label",ae({ref_for:!0},{active:H,selected:Q,option:$}),()=>[l("div",Ge,[l("div",null,L($.label),1),$.label!=$.description?(_(),k("div",{key:0,class:"text-xs text-gray-700",innerHTML:$.description},null,8,Me)):z("",!0)])])],2)]),_:2},1032,["value"]))),128))])),[[oe,b.items.length>0]])),128)),C.value.length==0?(_(),k("li",Je," No results found ")):z("",!0)]),_:3}),i(x).footer?(_(),k("div",We,[U(s.$slots,"footer",j(D({value:(q=y.value)==null?void 0:q.el._value,close:n})))])):z("",!0)])],512),[[oe,o]])]}),_:3},8,["show"])]),_:3},8,["modelValue"]))}},Qe={class:"space-y-1.5"},Xe={__name:"Link",props:{doctype:{type:String,required:!0},filters:{type:Object,default:()=>({})},modelValue:{type:String,default:""}},emits:["update:modelValue","change"],setup(f,{emit:p}){const c=f,a=p,t=Z(),r=T(()=>"value"in t),u=T({get:()=>r.value?t.value:c.modelValue,set:n=>(n==null?void 0:n.value)&&a(r.value?"change":"update:modelValue",n==null?void 0:n.value)}),y=I(null),m=I("");re(()=>{var n;return(n=y.value)==null?void 0:n.query},n=>{n=n||"",m.value!==n&&(m.value=n,d(n))},{debounce:300,immediate:!0}),re(()=>c.doctype,()=>d(""),{debounce:300,immediate:!0});const x=A({url:"frappe.desk.search.search_link",cache:[c.doctype,m.value],method:"POST",auto:!0,params:{txt:m.value,doctype:c.doctype,filters:c.filters},transform:n=>n.map(C=>({label:C.value,value:C.value,description:C.description}))});function d(n){x.update({params:{txt:n,doctype:c.doctype,filters:c.filters}}),x.reload()}const S=T(()=>[{sm:"text-xs",md:"text-base"}[t.size||"sm"],"text-gray-600"]);return(n,C)=>(_(),k("div",Qe,[i(t).label?(_(),k("label",{key:0,class:G(["block",S.value])},L(i(t).label),3)):z("",!0),g(Ke,{ref_key:"autocomplete",ref:y,options:i(x).data,modelValue:u.value,"onUpdate:modelValue":C[0]||(C[0]=w=>u.value=w),size:i(t).size||"sm",variant:i(t).variant,placeholder:i(t).placeholder,filterable:!1},ke({target:h(({open:w,togglePopover:V})=>[U(n.$slots,"target",j(D({open:w,togglePopover:V})))]),prefix:h(()=>[U(n.$slots,"prefix")]),"item-prefix":h(({active:w,selected:V,option:P})=>[U(n.$slots,"item-prefix",j(D({active:w,selected:V,option:P})))]),"item-label":h(({active:w,selected:V,option:P})=>[U(n.$slots,"item-label",j(D({active:w,selected:V,option:P})))]),_:2},[i(t).onCreate?{name:"footer",fn:h(({value:w,close:V})=>[l("div",null,[g(i(ne),{variant:"ghost",class:"w-full !justify-start",label:"Create New",onClick:P=>i(t).onCreate(w,V)},{prefix:h(()=>[g(i(we),{class:"h-4 w-4 stroke-1.5"})]),_:2},1032,["onClick"])])]),key:"0"}:void 0]),1032,["options","modelValue","size","variant","placeholder"])]))}},Ye={class:"grid place-content-center"},Ze={class:"flex-col w-96 pt-10"},et={class:"p-2"},tt={class:"p-2"},st={class:"p-2"},lt={class:"p-2"},at={class:"p-2"},ot={class:"p-2 text-center",required:!0},rt={class:"mb-4"},nt={key:1,class:"mb-4"},it={class:"flex items-center"},ut={class:"border rounded-md p-2 mr-2"},ct={class:"flex flex-col"},dt={class:"p-2 text-center",required:!0},mt={class:"mb-4"},pt={key:1,class:"mb-4"},ft={class:"flex items-center"},vt={class:"border rounded-md p-2 mr-2"},gt={class:"flex flex-col"},_t={class:"text-center p-5"},yt={__name:"App",setup(f){const p=new URL(window.location.href),c=new URLSearchParams(p.search);let t=Object.fromEntries(c).name;const r=Ce("$translate"),u=I(""),y=I(""),m=I(""),x=I(""),d=Y({ticket_image:null,invoice_image:null,travelDoc:""});d.travelDoc=t;const S=s=>{d.ticket_image=s},n=()=>{d.ticket_image=null},C=s=>{d.invoice_image=s},w=()=>{d.invoice_image=null};function V(s){let e=s.name.split(".").pop().toLowerCase();if(!["png","jpg","jpeg"].includes(e))return r("Only PNG and JPG images are allowed")}const P=Ve({doctype:"Project Travel Request",fields:["name","bill_amount","service_charge","ticket_attachment","invoice_attachment","supplier_invoice_number","supplier_invoice_date"]});function F(){var s,e;P.setValue,P.setValue.submit({name:d.travelDoc,supplier_invoice_date:u.value,supplier_invoice_number:y.value,bill_amount:m.value,service_charge:x.value,ticket_attachment:((s=d.ticket_image)==null?void 0:s.file_url)||"",invoice_attachment:((e=d.invoice_image)==null?void 0:e.file_url)||""},{onSuccess(){window.location.replace("/success-page"),console.log("Successs")},onError(){console.log("Error!!")}},u.value="",y.value="",d.travelDoc="",m.value="",x.value="",d.ticket_image=null,d.invoice_image=null)}return(s,e)=>{const v=$e("Button");return _(),k("div",Ye,[l("div",Ze,[e[12]||(e[12]=l("p",{class:"text-3xl p-2 text-center"},"Project Travel Request",-1)),l("div",null,[l("div",et,[g(Xe,{modelValue:d.travelDoc,"onUpdate:modelValue":e[0]||(e[0]=o=>d.travelDoc=o),doctype:"Project Travel Request",label:"Project Travel Request",required:!0,filters:{docstatus:0}},null,8,["modelValue"])]),l("div",tt,[g(i(B),{type:"date",ref_for:!0,size:"md",variant:"subtle",placeholder:"Supplier Invoice Date",disabled:!1,required:!0,label:"Supplier Invoice Date",modelValue:u.value,"onUpdate:modelValue":e[1]||(e[1]=o=>u.value=o)},null,8,["modelValue"])]),l("div",st,[g(i(B),{type:"text",ref_for:!0,size:"md",variant:"subtle",placeholder:"Supplier Invoice Number",disabled:!1,label:"Supplier Invoice Number",modelValue:y.value,"onUpdate:modelValue":e[2]||(e[2]=o=>y.value=o)},null,8,["modelValue"])]),l("div",lt,[g(i(B),{type:"text",ref_for:!0,size:"md",variant:"subtle",placeholder:"Bill Amount",disabled:!1,label:"Bill Amount",required:!0,modelValue:m.value,"onUpdate:modelValue":e[3]||(e[3]=o=>m.value=o)},null,8,["modelValue"])]),l("div",at,[g(i(B),{type:"text",ref_for:!0,size:"md",variant:"subtle",placeholder:"Service Charges",disabled:!1,label:"Service Charges",modelValue:x.value,"onUpdate:modelValue":e[4]||(e[4]=o=>x.value=o),required:""},null,8,["modelValue"])]),l("div",ot,[d.ticket_image?(_(),k("div",nt,[e[9]||(e[9]=l("div",{class:"text-xs text-gray-600 mb-1"},L("Ticket"),-1)),l("div",it,[l("div",ut,[g(i(ue),{class:"h-5 w-5 stroke-1.5 text-gray-700"})]),l("div",ct,[l("span",null,L(d.ticket_image.file_name),1)]),g(i(M),{onClick:e[6]||(e[6]=o=>n()),class:"bg-gray-200 rounded-md cursor-pointer stroke-1.5 w-5 h-5 p-1 ml-4"})])])):(_(),N(i(ie),{key:0,fileTypes:["image/*"],validateFile:V,onSuccess:e[5]||(e[5]=o=>S(o))},{default:h(({file:o,progress:q,uploading:b,openFileSelector:$})=>[l("div",rt,[g(v,{onClick:$,loading:b},{default:h(()=>[J(L(b?`Uploading ${q}%`:"Upload a Ticket"),1)]),_:2},1032,["onClick","loading"])])]),_:1}))]),l("div",dt,[d.invoice_image?(_(),k("div",pt,[e[10]||(e[10]=l("div",{class:"text-xs text-gray-600 mb-1"},L("Invoice"),-1)),l("div",ft,[l("div",vt,[g(i(ue),{class:"h-5 w-5 stroke-1.5 text-gray-700"})]),l("div",gt,[l("span",null,L(d.invoice_image.file_name),1)]),g(i(M),{onClick:e[8]||(e[8]=o=>w()),class:"bg-gray-200 rounded-md cursor-pointer stroke-1.5 w-5 h-5 p-1 ml-4"})])])):(_(),N(i(ie),{key:0,fileTypes:["image/*"],validateFile:V,onSuccess:e[7]||(e[7]=o=>C(o))},{default:h(({file:o,progress:q,uploading:b,openFileSelector:$})=>[l("div",mt,[g(v,{onClick:$,loading:b},{default:h(()=>[J(L(b?`Uploading ${q}%`:"Upload a Invoice"),1)]),_:2},1032,["onClick","loading"])])]),_:1}))])]),l("div",_t,[g(v,{class:"p-2",variant:"solid",ref_for:!0,theme:"gray",size:"md",label:"Button",loading:!1,loadingText:null,disabled:!1,onClick:F},{default:h(()=>e[11]||(e[11]=[J(" Send Request ")])),_:1})])])])}}};let R=Le(yt);Se("resourceFetcher",Ie);R.use(O);R.use(Pe);R.component("Button",ne);R.component("Card",qe);R.component("Input",Te);R.mount("#app");export{E as s};
