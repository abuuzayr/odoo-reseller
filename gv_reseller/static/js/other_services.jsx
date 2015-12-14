var otsvTmpl = {
	'Email Hosting': {
		title: 'Email Hosting',
		description: 'Lorem Ipsum .. candy Waffers and Ear plugs too',
		price: '120',
		extra: '10GB'
	},
	'Website Domain1':{		
		title: 'Website Domain(.COM)',
		description: 'Lorem Ipsum .. candy Waffers and Ear plugs too',
		price: '20',
		extra: '.COM'
	},
	'Website Domain2':{		
		title: 'Website Domain(.COM.SG)',
		description: 'Lorem Ipsum .. candy Waffers and Ear plugs too',
		price: '60',
		extra: '.COM.SG'
	},
	'Website Domain3':{		
		title: 'Website Domain(.SG)',
		description: 'Lorem Ipsum .. candy Waffers and Ear plugs too',
		price: '20',
		extra: '.SG'
	},
	'Website Design':{	
		title: 'Website Design',
		description: 'Lorem Ipsum .. candy Waffers and Ear plugs too',
		price: 1000,
		extra: [{
			pages: 10,
			price: 0
		},{
			pages: 20,
			price: 500
		}]
	}
};

(function(__myglobal){	
	var ServiceTypes = Object.keys(otsvTmpl);
	var classNames = window.classNames;

	var OstSD = React.createClass({
		updateSelected: function(sel){
			this.setState({selected:sel});
			this.refs.ul.blur();
			this.props.updateDesignPrice(sel);
		},
		getInitialState: function(){
			return {selected:0};
		},
		render: function(){
			return (
			<div>
				<ul ref="ul" tabIndex="-1" className="opt_serv_dropdown">
					<li>
						Up to {otsvTmpl['Website Design'].extra[this.state.selected].pages} pages
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
			this.setState({extraPrice: otsvTmpl['Website Design'].extra[sel].price});
			this.props.updateState(sel);
		},
		getInitialState: function(){
			return {extraPrice:0};
		},
		render: function(){			
			return (				
				<div className="ots">
					<div className="top" onClick={this.props.updateState}>
						<input type="checkbox" checked={this.props.selected === true} onChange={this.updateState} />
					</div>
					<header>{this.props.title}</header>
					<p>{this.props.dat.description}</p>
					<span className="price">
						<span>${(parseFloat(this.props.dat.price) + this.state.extraPrice)}</span>
						<span>{typeof this.props.dat.price === "number" ? "" : " / YR"}</span>
					</span>
					<span className="ext">
						{typeof this.props.dat.extra === "string" ? this.props.dat.extra : <OstSD updateDesignPrice={this.updateDesignPrice}/> }
					</span>
				</div>
			)
		}
	});

	var OstCon = React.createClass({
		updateState: function(v, wd){
			var obj = {};
			var serviceObj = otsvTmpl[v];

			if (v === 'Website Design' && typeof wd === "number"){
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
					var obj; obj[v] = s;
					ctx.setState(obj);
				};
				__myglobal[v].getState = function(s){
					return ctx.state[obj];
				};
			});
			__myglobal['Website Design'].setPages = function(v){
				var obj = {webdesign: v};
				ctx.setState(obj);
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