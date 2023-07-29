import { Component, OnInit,Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ThrowStmt } from '@angular/compiler';
import { GlobalConstants } from 'src/app/global/mariosGlobal/mariosGlobal'

@Component({
  selector: 'ami-fullstack-row-product',
  templateUrl: './row-product.component.html',
  styleUrls: ['./row-product.component.scss']
})
export class RowProductComponent implements OnInit {

  @Input() ProductName : any ;
  @Input()  ProductQuant: any ;
  @Input()  ProductExpiringDate: any ; 
  @Input()  ProductLocationStart: any ;
  @Input()  ProductLocationEnd: any ;
  @Input()  ProductShelf: any ;
  @Input()  ProductUserLastUsed: any ;
  @Input()  ProductWhenLastUsed: any ;
  @Input()  ProductDaysToExpire: any ;
  @Input()  ProductOriginalQuantity : any; 
  
  ProductFotos  : any;
  ProductSymbol : any;
  LeftLabelColor : any ; 
  isLowQuantity : any ; 
  isExpiring : any ;
  colorForHTTPrequest : any ; 
  today : any = new Date();

  timeIcon = "../../assets/images_marios/icons8-clock-32-black.png" ; // const
  quantIcon = "../../assets/images_marios/icons8-cookie-32-black.png" ; // const

  constructor(private http: HttpClient,private globalConst: GlobalConstants) { }

  ngOnInit() {
    this.decideFoto(this.ProductName);
    this.decideIcon(this.ProductQuant , this.ProductDaysToExpire);
    // this.decideExpiringDate(this.ProductExpiring);
    this.changeToYesterdayIfNeeded(); // unused
  }

  //unused
  public changeToYesterdayIfNeeded(){
    if (this.ProductWhenLastUsed == 1){
      this.ProductWhenLastUsed = 'Yesterday' ; // unused 
    }
  }

  public LightItemFunc(){ // When Locate button is pressed
   
    // here make a post HTTP request to blink lights in cupboard
    // alert('Lighting up the item in cupboard');
    
    const body = { 
    'ledstripeId': 1, // inside Cupboard is lestripe = 1 
    'startLed': this.ProductLocationStart,
    'endLed' : this.ProductLocationEnd,
    'color' : this.colorForHTTPrequest 
    };

    this.http.post<any>('http://139.91.96.156/lights/ConstantFromToLedIDs', body).subscribe(data => { // CAUTION ! IP could be changed 
      console.log('Received data is : ' , data) ;
    });

    // Open cupboard fully
    this.http.post<any>('http://139.91.96.156/door/open',{}).subscribe(data => {
      console.log('Door is opening ...');
    }) // CAUTION ! IP could be changed
  }

  public decideFoto(ProductLabel : any){
    if (ProductLabel == "Coffee"){
      this.ProductFotos = "assets/images_marios/Coffee.png" ; 
    }
    else if (ProductLabel == "Rice"){
      this.ProductFotos = "assets/images_marios/Rice.png" ; 
    }
    else if (ProductLabel == "Sugar"){
      this.ProductFotos = "assets/images_marios/Sugar.png" ; 
    }
    else if (ProductLabel == "Vinegar"){
      this.ProductFotos = "assets/images_marios/Vinegar.png" ; 
    }
    else if (ProductLabel == "Merenda"){
      this.ProductFotos = "assets/images_marios/Merenda.png" ; 
    }
    else if (ProductLabel == "Tomato"){
      this.ProductFotos = "assets/images_marios/Tomato.png" ; 
    }
    else if (ProductLabel == "Mustard"){
      this.ProductFotos = "assets/images_marios/Mustard.png" ; 
    }
    else if (ProductLabel == "Corn"){
      this.ProductFotos = "assets/images_marios/Corn.png" ; 
    }
    else if (ProductLabel == "Mayo"){
      this.ProductFotos = "assets/images_marios/Mayo.png" ; 
    }
    else if (ProductLabel == "Beans"){
      this.ProductFotos = "assets/images_marios/Beans.png" ; 
    }
    else if (ProductLabel == "Salt"){
      this.ProductFotos = "assets/images_marios/Salt.png" ; 
    }
    else if (ProductLabel == "Mushroom"){
      this.ProductFotos = "assets/images_marios/Mushroom.png" ; 
    }
    else{
      console.log('Some error heree marios')
    }
  }

  public decideIcon(ProductQuantity : any , daysToExpire : any ){

    if (daysToExpire < this.globalConst.expiringThreshold ){
      this.ProductSymbol = "../../assets/images_marios/icons8-clock-32.png" ;
      this.LeftLabelColor = "#FB0404"; // red
      this.colorForHTTPrequest = "red" ; 
      this.isExpiring = true ; 
    }
    else if (ProductQuantity < this.globalConst.lowQuantityPercentageThreshold * this.ProductOriginalQuantity){
      this.LeftLabelColor = "#ECA131"; // orange
      this.colorForHTTPrequest = "yellow" ; 
      this.ProductSymbol = "../../assets/images_marios/icons8-cookie-32.png" ;
      this.isLowQuantity = true ;
    }
    else{
      this.LeftLabelColor = "#32925E"; // green
      this.colorForHTTPrequest = "green" ;
      this.ProductSymbol = "../../assets/images_marios/icons8-ok-32.png" ;
    }
  }

}

