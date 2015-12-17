(function(__myglobal){	
	var ServiceTypes = Object.keys(otsvTmpl);
	var classNames = window.classNames;

	var OstSD = React.createClass({
		updateSelected: function(sel){
			this.refs.ul.blur();
			this.props.updateDesignPrice(sel);
		},
		render: function(){
			return (
			<div>
				<ul ref="ul" tabIndex="-1" className="opt_serv_dropdown">
					<li>
						Up to {otsvTmpl['Website Design'].extra[this.props.wd].pages} pages
					</li>
					<li onClick={this.updateSelected.bind(this, 0)}>Up to 10 pages</li>
					<li onClick={this.updateSelected.bind(this, 1)}>Up to 20 pages</li>
				</ul>			
				<br className="clear"/>
			</div>
			);
		}
	});

	var OstCb = React.createClass({
		render: function(){
			return (<input type="checkbox" value={this.props.selected} onChange={this.props.updateState}/>)
		}
	});

	var OstDiv = React.createClass({
		updateDesignPrice: function(sel){
			this.props.updateState(sel);
		},
		render: function(){
			var ctx = this;
			var extraPrice = typeof this.props.dat.extra === "string" ? 0 : parseFloat(otsvTmpl['Website Design'].extra[this.props.wd].price)
			return (
				<div className="ots">
					<div className="top" onClick={this.props.updateState}>
						<input type="checkbox" checked={this.props.selected === true} onChange={this.updateState} />
					</div>
					<header>{this.props.title}</header>
					<p>{this.props.dat.description}</p>
					{getPriceTag()}
					<span className="ext">
						{typeof this.props.dat.extra === "string" ? this.props.dat.extra : <OstSD wd={this.props.wd} updateDesignPrice={this.updateDesignPrice}/> }
					</span>
				</div>
			)
			function getPriceTag(){
				if (isRSA) {
					return (
						<span className="price">
							<span>${(parseFloat(ctx.props.dat.price) + extraPrice )}</span>
							<span>{typeof ctx.props.dat.price === "number" ? "" : " / YR"}</span>
						</span>
					);
				} else {
					return;
				}
			}
		}
	});

	var OstCon = React.createClass({
		updateState: function(v, wd){
			var obj = {};
			var serviceObj = otsvTmpl[v];

			if (v === 'Website Design' && typeof wd === "number"){
				console.log(wd);
				obj.webdesign = wd;

				if (this.state[v] === false) {
					obj[v] = true;
					__myglobal.summary.addService(serviceObj,{'wd':wd});
				} else {					
					__myglobal.summary.removeService(serviceObj);
					__myglobal.summary.addService(serviceObj,{'wd':wd});
				}
			} else {			
				obj[v] = !this.state[v];	
				if (obj[v] === true){				
					__myglobal.summary.addService(serviceObj);
				} else {
					__myglobal.summary.removeService(serviceObj);
				}
			}

			this.setState(obj);
		},
		componentWillMount: function(){
			var ctx = this;
			ServiceTypes.forEach(function(v){
				__myglobal[v] = {};
				__myglobal[v].setState = function(s){
					ctx.updateState(v,s);
				};
				__myglobal[v].getState = function(s){
					return ctx.state[obj];
				};
			});
			__myglobal['Website Design'].setPages = function(v){
				ctx.updateState('Website Design', v);
			};
			__myglobal['Website Design'].getPages = function(v){
				return ctx.state.webdesign;
			};
		},
		getInitialState: function(){
			return ServiceTypes.reduce(function(prev,curr){
				prev[curr] = false;
				return prev;
			}, {webdesign: 0});
		},
		render: function(){
			var ctx = this;
			return (
				<div>
					{ServiceTypes.map(function(v){
						return <OstDiv
							key={v}
							title={v}
							dat={otsvTmpl[v]}
							selected={ctx.state[v]}
							wd={ctx.state.webdesign}
							updateState={ctx.updateState.bind(ctx, v)}
							>
						</OstDiv>
					})}
				</div>
			)
		}
	});

	ReactDOM.render(
		React.createElement(OstCon),		
		document.getElementById('ots_container')
	)
})(__rsGlobal);