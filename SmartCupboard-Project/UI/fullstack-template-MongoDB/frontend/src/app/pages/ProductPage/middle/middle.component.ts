import { Component, OnInit,Input } from '@angular/core';

@Component({
  selector: 'ami-fullstack-middle',
  templateUrl: './middle.component.html',
  styleUrls: ['./middle.component.scss']
})
export class MiddleComponent implements OnInit {


  @Input() productData : any ; 

  constructor() { }

  ngOnInit() {
  }

}
