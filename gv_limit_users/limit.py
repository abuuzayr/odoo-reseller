from openerp import fields, models, api, exceptions, osv


class gv_user_limit(models.Model):
    """
    For limiting the number of employees that can be created. Limit can only be set by superadmin on settings after having logged in.
    Overwrites the write and create methods.
    Employees are determined by the computed field 'share'
    Adding api.constrains to the computed field 'share' was proven not to work hence the method overriding.
    """
    _inherit="res.users"

    def _limit_users(self):          
        if not self.share:
            if self.active:
                # get total number of employees. Need to reduce the value by one because of superadmin account.
                totalNumberOfEmployees = len(self.env['res.users'].search([('active', '=', True), ('share', '=', False)])) -1
                userLimit = self.get_user_limit()
                print userLimit
                if totalNumberOfEmployees > userLimit:
                    errorMsg = "You have reached the maximum number of employees allowable. Max: " + str(userLimit) + " Current: " + str(totalNumberOfEmployees)
                    raise exceptions.ValidationError(errorMsg)
                
    def get_user_limit(self):
        config_array = self.env['gv.config.settings'].search([], limit=1, order='id DESC')
        if config_array:
            return config_array[0].userLimit
        return 0

    @api.multi
    def write(self, values):
        self._limit_users()
        return super(gv_user_limit, self).write(values)
    
    @api.one
    def create(self, values):
        self._limit_users()
        return super(gv_user_limit, self).create(values)
    
class gv_config_settings(osv.osv.osv_memory):
    """
    Adds the maximum number of employees limit to the settings, which will be saved for the configuration.
    """
    _inherit = 'res.config.settings'
    _name="gv.config.settings"
    
    userLimit = fields.Integer(string="Maximum No of Employees", help="Maximum number of active employees allowable for this installation. ")
    
    def get_default_userLimit(self, cr, uid, ids, context=None):
        """
        Retrieves and displays the limit from gv.config.settings. 
        """
        config_obj = self.pool.get('gv.config.settings')
        config_ids = config_obj.search(cr, uid, [], limit=1, order='id DESC', context=context)
        if config_ids:
            config = config_obj.browse(cr, uid, config_ids[0], context=context)
            return {'userLimit': config.userLimit}
        return {}
    
 
    def set_default_userLimit(self, cr, uid, ids, context=None):
        """
        saves the userLimit to gv.config.settings. Will be automatically called when the "Apply" button is clicked" 
        """
        config_obj = self.pool.get('gv.config.settings')
        config_ids = config_obj.search(cr, uid, [], limit=1, order='id DESC', context=context)
        config = self.browse(cr, uid, ids[0], context)
        config_obj.write(cr, uid, config_ids[0], {'userLimit': config.userLimit})
