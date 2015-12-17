(function(__myglobal){
	var SummItem = React.createClass({
		render: function(){
			var total = 0;
			var ctx = this;
			var count = ctx.props.data.length;

			if (!!ctx.props.data2) {count = count + ctx.props.data2.length; }
			if (ctx.props.title === 'Users') { count = ctx.props.data[0]; total = count * per_user_price }
			if (ctx.props.title === 'Modules') {
				if (count < 2) {
					total = 1200;
				} else {
					total = count * 600;
				}
			} else if (ctx.props.hasOwnProperty('data')) {
				ctx.props.data.forEach(function(v){
					if (v.hasOwnProperty('extra') && typeof v.extra === "object") {
						total = total + parseFloat(v.price) + v.extra[ctx.props.wd].price;
					} else if (v.hasOwnProperty('price')){
						total = total + parseFloat(v.price);
					} else if (v.hasOwnProperty('base')){
						total = total + parseFloat(v.base);
					}
				});
			}
			if (ctx.props.hasOwnProperty('data2')) {
				ctx.props.data2.forEach(function(v){
					if (v.hasOwnProperty('lstPrice')) {
						total = total + parseFloat(v.lstPrice);
					}
				});
			}

			return (
				<div className="row">
					{render()}
				</div>
			);

			function render(){
				if (isRSA) {
					return (<div>
							<div className="col-sm-6">{count} x {ctx.props.title}</div>
							<div className="col-sm-6">${total}</div></div>
						);
				} else {
					return (<div className="col-sm-12">{count} x {ctx.props.title}</div>);
				}
			}
		}
	});

	var SummCon = React.createClass({
		componentDidUpdate: function(){
			__myglobal.util.updateTotal();
		},
		componentWillMount: function(){
			var ctx = this;
			__myglobal.summary = {};
			__myglobal.summary.setUsers = function(count){
				ctx.setState({users:[count]});
			}
			__myglobal.summary.addModule = function(mod){
				var newState = {modules: ctx.state.modules};
				newState.modules.push(mod);
				ctx.setState(newState);
			};
			__myglobal.summary.removeModule = function(opt){
				var newModules = ctx.state.modules;
				if (newModules.indexOf(opt) > -1) {
					newModules.splice(newModules.indexOf(opt), 1);
					ctx.setState({modules: newModules});
				}
			};
			__myglobal.summary.addService = function(serv, options){
				var newState = {};
				if (!!options && options.hasOwnProperty('wd')){
					newState.wd = options.wd;
				}
				newState.services = ctx.state.services;
				newState.services.push(serv);
				ctx.setState(newState);
			};
			__myglobal.summary.removeService = function(serv){
				var servState = ctx.state.services;
				if (servState.indexOf(serv) > -1) {
					servState.splice(servState.indexOf(serv), 1);
					ctx.setState({services: servState});
				}
			};
			__myglobal.summary.addOptional = function(opt){
				var newState = {optional: ctx.state.optional};
				newState.optional.push(opt);
				ctx.setState(newState);
			};
			__myglobal.summary.removeOptional = function(opt){
				var newOptional = ctx.state.optional;
				if (newOptional.indexOf(opt) > -1) {
					newOptional.splice(newOptional.indexOf(opt), 1);
					ctx.setState({optional: newOptional});
				}
			};
			__myglobal.summary.getServicePrice = function(){
				var total = 0;
				
				ctx.state.services.forEach(function(v){
					if (v.hasOwnProperty('extra') && typeof v.extra === "object") {	
						total = total + parseFloat(v.price) + v.extra[ctx.state.wd].price;
					} else if (v.hasOwnProperty('price')){
						total = total + parseFloat(v.price);
					}
				});
				
				ctx.state.optional.forEach(function(v){
					if (v.hasOwnProperty('lstPrice')) {
						total = total + parseFloat(v.lstPrice);
					}
				});

				return total;
			};
			__myglobal.summary.getModulePrice = function(){
				if (ctx.state.modules.length === 1){
					return 0;
				} else if (ctx.state.modules.length === 1) {
					return 1200;
				} else {
					return 600 * ctx.state.modules.length; 
				}
			};
			__myglobal.summary.getUsersPrice = function(){
				return ctx.state.users[0] * per_user_price;
			};
			__myglobal.summary.getState = function(){
				return ctx.state;
			}
		},
		componentDidMount: function(){
			__myglobal.util.updateTotal();
		},
		getInitialState: function(){
			return {
				users: [1],
				modules: [],
				optional: [],
				services: [],
				wd: 0
			};
		},
		render: function(){
			var ctx = this;
			var hasUsers = this.state.users.length;
			var hasModules = this.state.modules.length;
			var hasOptional = this.state.optional.length;
			var hasServices = this.state.services.length;
			var totalCount = hasUsers + hasModules + hasServices + hasOptional;
			return (
				<div className="summary_list">
					{(hasUsers > 0) ? <SummItem title="Users" data={ctx.state.users} />  : "" }
					{(hasModules > 0) ? <SummItem title="Modules" data={ctx.state.modules} /> : "" }
					{(hasServices > 0 || hasOptional > 0) ? <SummItem title="Services" data2={ctx.state.optional} data={ctx.state.services} wd={ctx.state.wd} />  : "" }
					{(totalCount < 1) ? <p>No Modules or Services Selected</p>: ""}
				</div>
			);
		}
	});

	ReactDOM.render(
		React.createElement(SummCon),
		document.getElementById('summary_list_modules')		
	);

	__myglobal.observer.notify();
})(__rsGlobal);