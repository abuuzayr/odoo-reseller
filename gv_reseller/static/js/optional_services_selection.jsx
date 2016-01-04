//Optional Services Recommendataions
(function(__myglobal){
	var recommendations = [
		{
			name: 'SME Basic',
			moduleCount: [1,1],
			selected: [0,-1,-1,-1]
		},
		{
			name: 'SME Basic+',
			moduleCount: [1,1],
			selected: [0,0,-1,-1]
		},
		{
			name: 'SME Starter',
			moduleCount: [2,3],
			selected: [1,1,1,1]
		},
		{
			name: 'SME Assist',
			moduleCount: [4,6],
			selected: [2,2,2,2]
		},
		{
			name: 'SME Pro',
			moduleCount: [7,8],
			selected: [3,3,3,3]
		}
	];

	var OsDiv = React.createClass({
		render: function(){
			return (				
				<div className="ots">
					<div className="top">
						<input type="checkbox"
							onClick={this.props.onSelect}
							checked={this.props.selected} />
					</div>
					<header>
						{this.props.dat.name}
					</header>
				</div>
			)
		}
	});

	var OsCon = React.createClass({
		updateSelected: function(v){
			__myglobal.Implementation.setState(v.selected[0]);
			__myglobal.Coordination.setState(v.selected[1]);
			__myglobal.Consultation.setState(v.selected[2]);
			__myglobal.Training.setState(v.selected[3]);

			this.setState({selected:recommendations.indexOf(v)});
		},
		componentWillMount: function(){
			var ctx = this;
			__myglobal.UnsetRecomm = function(){
				ctx.setState({selected:-1});
			}
		},
		getInitialState: function(){			
			return {
				selected: -1
			};
		},
		render: function(){
			var ctx = this;
			return (
				<div>
					{recommendations.map(function(v){
					return (
						<OsDiv 
							key={recommendations.indexOf(v)}
							selected={ctx.state.selected === recommendations.indexOf(v)}
							dat={v}
							onSelect={ctx.updateSelected.bind(ctx,v)}/>
					)
					})}
				</div>
			);
		}
	});

	ReactDOM.render(
		React.createElement(OsCon),
		document.getElementById('os_container_pre')
	);
})(__rsGlobal);