import { Component, OnInit,Input } from '@angular/core';
import {Router} from '@angular/router'
import { GlobalConstants } from 'src/app/global/mariosGlobal/mariosGlobal'

@Component({
  selector: 'ami-fullstack-product-pos',
  templateUrl: './product-pos.component.html',
  styleUrls: ['./product-pos.component.scss']
})
export class ProductPosComponent implements OnInit {

  @Input() ProductName : any;
  @Input() ProductQuant : any;
  @Input() ProductExpiring : any; // daysToExpire
  @Input() ProductOriginalWeight : any;

  ProductFotos  : any;
  ProductSymbol : any;
  LeftLabelColor : any ; 
  isLowQuantity : any ; 
  
  constructor(private router:Router,private globalConst: GlobalConstants) { }

  ngOnInit() {
    this.decideFoto(this.ProductName);
    this.decideIcon(this.ProductQuant , this.ProductExpiring, this.ProductOriginalWeight);
  }

  // Navigation to Product Page ... 0.5 seconds after click event
  public navigateToProductPage(productName: any) {
    setTimeout(() => {
      this.router.navigate(['/ProductPage'] , {state: {data: productName} });
    },
      500); // mseconds
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
    else if (ProductLabel == "Tomato"){
      this.ProductFotos = "assets/images_marios/Tomato.png" ; 
    }
    else if (ProductLabel == "Vinegar"){
      this.ProductFotos = "assets/images_marios/Vinegar.png" ; 
    }
    else if (ProductLabel == "Merenda"){
      this.ProductFotos = "assets/images_marios/Merenda.png" ; 
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
      console.log('Mushroommmmmm');
      console.log(this.ProductFotos);
    }
    else{
      console.log('Some error here check product-pos')
    }
  }

  public decideIcon(ProductQuantity : any , ProductExpiringDays : any , ProductOriginalWeight : any){
    if (ProductExpiringDays < this.globalConst.expiringThreshold ){
      this.ProductSymbol = "../../assets/images_marios/icons8-clock-32.png" ;
      this.LeftLabelColor = "#FB0404"; // red
    }
    else if (ProductQuantity < this.globalConst.lowQuantityPercentageThreshold * ProductOriginalWeight){
      this.LeftLabelColor = "#ECA131"; // orange 
      this.ProductSymbol = "../../assets/images_marios/icons8-cookie-32.png" ;
      this.isLowQuantity = true ;
    }
    else{
      this.LeftLabelColor = "#32925E"; // green
      this.ProductSymbol = "../../assets/images_marios/icons8-ok-32.png" ;

    }
  }

}