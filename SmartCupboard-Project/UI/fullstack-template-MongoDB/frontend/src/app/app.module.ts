import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './app.routing';
import { TopBarComponent } from './pages/HomePage/top-bar/top-bar.component';
import { BottomBarComponent } from './pages/HomePage/bottom-bar/bottom-bar.component';
import { ProductPosComponent } from './pages/HomePage/product-pos/product-pos.component';
import { MiddleBarComponent } from './pages/HomePage/middle-bar/middle-bar.component';
import { ColumnMiddleOneComponent } from './pages/HomePage/column-middle-one/column-middle-one.component';
import { ColumnMiddleTwoComponent } from './pages/HomePage/column-middle-two/column-middle-two.component';
import { ProductPageComponent } from './pages/ProductPage/product-page/product-page.component';
import { HomeComponent } from './pages/HomePage/home/home.component';
import { TopComponent } from './pages/ProductPage/top/top.component';
import { BottomComponent } from './pages/ProductPage/bottom/bottom.component';
import { MiddleComponent } from './pages/ProductPage/middle/middle.component';
import { RowProductComponent } from './pages/ProductPage/row-product/row-product.component';
import { StatMainComponent } from './pages/StatsPage/stat-main/stat-main.component';
import { TopStatComponent } from './pages/StatsPage/top-stat/top-stat.component';
import { BottomStatComponent } from './pages/StatsPage/bottom-stat/bottom-stat.component';
import { MiddleStatComponent } from './pages/StatsPage/middle-stat/middle-stat.component';

import {GlobalConstants} from 'src/app/global/mariosGlobal/mariosGlobal';
import { DisplayCupboardsPageComponent } from './pages/DisplayCupboardspage/display-cupboards-page.component';
import { AmiPageComponent } from './pages/AmiPage/ami-page.component';
import { ModeratorPageComponent } from './pages/ModeratorPage/moderator-page.component';


@NgModule({
  declarations: [
    AppComponent,
    TopBarComponent,
    BottomBarComponent,
    ProductPosComponent,
    MiddleBarComponent,
    ColumnMiddleOneComponent,
    ColumnMiddleTwoComponent,
    ProductPageComponent,
    HomeComponent,
    TopComponent,
    BottomComponent,
    MiddleComponent,
    RowProductComponent,
    StatMainComponent,
    TopStatComponent,
    BottomStatComponent,
    MiddleStatComponent,
    DisplayCupboardsPageComponent,
    AmiPageComponent,
    ModeratorPageComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule
  ],
  providers: [GlobalConstants],
  bootstrap: [AppComponent]
})
export class AppModule { }
